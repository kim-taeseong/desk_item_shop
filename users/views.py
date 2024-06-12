from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import CreateView, TemplateView, ListView
from django.contrib.auth import login, get_user_model, logout, authenticate, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.utils.translation import gettext as _
from django.utils import timezone
from cart.views import transfer_session_cart_to_user
from logistics.models import Product
from order.models import Order
from .models import User, Customer, Store
from .forms import CustomerSignUpForm, StoreSignUpForm, LoginForm, CustomerEditForm, StoreEditForm
from .decorators import customer_required, store_required

User = get_user_model()

# Customer 회원가입
class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'customer/customer_signup.html' # Customer 회원가입 페이지로 이동

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('users:signup_done')
    
# Store 회원가입
class StoreSignUpView(CreateView):
    model = User
    form_class = StoreSignUpForm
    template_name = 'store/store_signup.html' # Store 회원가입 페이지로 이동

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'store'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        return redirect('users:signup_done')
    
# 회원가입 완료
class SignUpDoneView(TemplateView):
    template_name = 'login_password/signup_done.html'

# 로그인
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login_password/login.html'

    def dispatch(self, request, *args, **kwargs): 
        # 이미 로그인된 사용자가 login 페이지로 접근하면 logistics:main 페이지로 리다이렉트
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(reverse('logistics:main'))
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        # 비활성화된 계정으로 로그인 시도 시, 탈퇴한 계정 페이지로
        username = form.cleaned_data.get('username')
        user = User.objects.get(username=username)
        if user and not user.is_active:
            return HttpResponseRedirect(reverse('users:account_delete_alert'))
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_customer: # 아이디가 Customer라면 logistics:main 페이지로
                # 세션의 정보 데이터베이스로 이동
                transfer_session_cart_to_user(self.request, user)
                return reverse('logistics:main')
            elif user.is_store: # 아이디가 Store라면 store_home 페이지로
                return reverse('users:store_home')
        else: # 잘못 입력하면 다시
            return reverse('login') 

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('users:login')  # 로그인 화면으로 리다이렉트

# 회원 탈퇴 - 실제 삭제가 아닌 비활성화 is_active = 0
@login_required
def account_delete(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            user_email = user.email  # 사용자 이메일 주소
            user.is_active = False # 탈퇴(비활성화) 처리
            user.deactivetime = timezone.now() # 비활성화 했을 당시의 시간을 저장
            user.save()
            logout(request)
            if hasattr(user, 'store'): # 만약 탈퇴하려는 계정이 판매자 계정이라면
                Product.objects.filter(store=user.store).update(is_active=False) # 해당 store의 상품들을 비활성화
            # 이메일 발송
            send_mail(
                subject='Desker에서 귀하의 계정 탈퇴를 확인합니다.',
                message=f"""안녕하세요, {user.username}님.
                            귀하의 Desker 계정이 성공적으로 탈퇴되었습니다.
                            이용해 주셔서 감사합니다. 더 나은 서비스로 다시 만날 수 있기를 바랍니다.
                            감사합니다,
                            Desker 팀""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_email],
                fail_silently=False,
            )
            return redirect('users:login') # 탈퇴 후 로그인 페이지로 리다이렉트
        else:
            messages.error(request, '비밀번호가 틀렸습니다.')
            return render(request, 'account_delete/account_delete.html')
    return render(request, 'account_delete/account_delete.html')

# 탈퇴한 계정 페이지 - 회원탈퇴 해놓고 7일 이내 재 로그인시 표시(실제 로그인 처리되는것은 아니기에 last_login 시간에 반영 X)
def account_delete_alert(request):
    return render(request, 'account_delete/account_delete_alert.html')

# 탈퇴 취소 페이지 - 탈퇴 취소됨 is_active = 1
def account_delete_cancel(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 첫 진입 시 and 사용자가 아이디나 비밀번호를 입력하지 않았을 경우
        if not username or not password:
            messages.error(request, '탈퇴를 취소하려는 계정의 아이디와 비밀번호를 입력해주세요.')
            return render(request, 'account_delete/account_delete_cancel.html')

        try:
            user = User.objects.get(username=username, is_active=False)
            if user.check_password(password): # 비밀번호가 일치하는 경우
                user.is_active = True # 사용자의 활성화 상태를 True로 설정
                user.deactivetime = None  # 비활성화 했던 시간을 None으로 변경

                # store 계정인 경우엔 상품들을 다시 활성화
                if hasattr(user, 'store') and user.store:
                    Product.all_objects.filter(store=user.store).update(is_active=True)
                user.save() 
                messages.success(request, '회원 탈퇴가 취소되었습니다. 계정이 활성화되었습니다.')
                return redirect('users:login')  # 로그인 페이지로 리다이렉트
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.') # 비밀번호가 일치하지 않으면
        except User.DoesNotExist:
            messages.error(request, '해당하는 계정을 찾을 수 없습니다.') # 아이디가 일치하지 않으면

    return render(request, 'account_delete/account_delete_cancel.html')

# 즉시 탈퇴 페이지 - 즉시 DB에서 모든 정보 삭제
def account_delete_now(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 첫 진입 시 and 사용자가 아이디나 비밀번호를 입력하지 않았을 경우
        if not username or not password:
            messages.error(request, '즉시 탈퇴하려는 계정의 아이디와 비밀번호를 입력해주세요.')
            return render(request, 'account_delete/account_delete_now.html')

        try:
            user = User.objects.get(username=username)
            if user.check_password(password): # 비밀번호가 일치하는 경우
                if hasattr(user, 'store'): # store 계정인 경우 연결된 모든 상품 삭제
                    user.store.product_set.all().delete()   
                user.delete() # 계정 삭제
                messages.success(request, '계정이 성공적으로 삭제되었습니다.')
                return redirect('users:login')  # 로그인 페이지로 리다이렉트
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.') # 비밀번호가 일치하지 않으면
        except User.DoesNotExist:
            messages.error(request, '해당하는 계정을 찾을 수 없습니다.') # 아이디가 일치하지 않으면

    return render(request, 'account_delete/account_delete_now.html')

# Customer 홈
@login_required
@customer_required
def customer_home(request):
    orders = Order.objects.filter(customer=request.user.customer)
    context = {'orders': orders}
    return render(request, 'customer/customer_home.html', context)

# 아이디 찾기
def find_username(request):
    if request.method == 'POST':
        email = request.POST['email']
        users = User.objects.get(email=email)
        if users.exists():
            current_site = get_current_site(request)
            domain = current_site.domain
            protocol = 'https' if request.is_secure() else 'http'
            user = users.first()
            login_url = reverse('users:login')  # 로그인 화면
            login_url = f"{protocol}://{domain}{login_url}"  # 전체 URL 생성
            # 이메일 문구
            send_mail(
                subject='Desker에서 귀하의 계정 정보를 안내드립니다.',
                message=f"""안녕하세요, Desker 입니다!
                            귀하의 계정 아이디는 다음과 같습니다: "{user.username}"
                            로그인 화면으로 이동하려면 다음 링크를 클릭하세요: {login_url}
                            Desker와 함께 더욱 효율적인 업무 환경을 만들어 가세요.
                            만약 이 메일이 잘못 전송되었다고 생각되시거나, 추가적인 도움이 필요하시면 언제든지 저희 고객 지원팀으로 연락 주시기 바랍니다.
                            감사합니다, 
                            Desker 팀""",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
            )
            return render(request, 'find/find_username_done.html')  # 이메일 발송 완료시 발송 완료 페이지로 이동
        else:
            # 등록된 이메일이 아닐 경우, 에러 메시지와 함께 find_username 템플릿을 다시 렌더링
            return render(request, 'find/find_username.html', {'error': '해당 이메일로 등록된 사용자가 없습니다.'})
    else:
        # GET 요청 처리
        return render(request, 'find/find_username.html')

# Customer 회원정보 수정
@login_required
@customer_required
def edit_customer(request):
    # 현재 로그인한 고객과 연결된 Customer 객체
    customer = get_object_or_404(Customer, user=request.user)
    if request.method == 'POST':
        # 고객으로부터 입력받은 데이터와 파일 사용해 초기화
        form = CustomerEditForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():  # 폼이 유효할 경우
            updated_customer = form.save()  # 변경사항을 DB에 저장
            return redirect('users:edit_customer_done')  # 고객 회원정보수정 완료 페이지로 리다이렉션
    else:
        # POST 요청이 아니라면 CustomerEditForm이 Customer 인스턴스로 초기화되어 현재 정보를 Customer 정보 폼에 채움
        form = CustomerEditForm(instance=customer)
    return render(request, 'edit_profile/edit_customer.html', {'form': form})

# Customer 회원정보 수정완료
class EditCustomerDoneView(TemplateView):
    template_name = 'edit_profile/edit_customer_done.html'  # Customer 회원정보 수정완료 페이지

# Store 회원정보 수정
@login_required
@store_required
def edit_store(request):

    # 현재 로그인한 사용자와 연결된 Store 객체
    store = get_object_or_404(Store, user=request.user) 
    if request.method == 'POST':
        
        # 사용자로부터 입력받은 데이터와 파일 사용해 초기화
        form = StoreEditForm(request.POST, request.FILES, instance=store) 
        if form.is_valid():  # 폼이 유효할 경우
            updated_store = form.save()  # 변경 사항을 DB에 저장
            return redirect('users:edit_store_done')  # Store 회원정보수정 완료 페이지로 리다이렉션
    else:
        # POST 요청이 아니라면 StoreEditForm이 store 인스턴스로 초기화되어 현재 정보를 store 정보 폼에 채움
        form = StoreEditForm(instance=store)
    return render(request, 'edit_profile/edit_store.html', {'form': form})

# Store 회원정보 수정완료
class EditStoreDoneView(TemplateView):
    template_name = 'edit_profile/edit_store_done.html' # Store 회원정보 수정완료 페이지

# 비밀번호 수정
@login_required
def edit_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # 비밀번호 변경 후 세션 유지
            messages.success(request, '비밀번호가 성공적으로 변경되었습니다!')
            return redirect(reverse('users:edit_password_done'))
        else:
            messages.error(request, '오류를 수정해주세요.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'login_password/edit_password.html', {'form': form})


# store_home
class StoreDashboardView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'store/store_home.html'
    context_object_name = 'products'

    def get_queryset(self):
        # 로그인한 사용자의 Store에 연결된 최근에 등록된 상품 5개를 가져옴
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'store'):
            return Product.objects.filter(store=user.store).order_by('-product_date')[:5]
        else:
            return Product.objects.none()
        
    # context에 담아 템플릿으로 전달
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = context['products']
        products_with_discount = []
        for product in products:
            discounted_price = product.product_price * (1 - product.product_sale / 100)  # 할인율을 적용한 금액
            products_with_discount.append((product, discounted_price))
        context['products_with_discount'] = products_with_discount
        return context

# Customer 기준의 store_home
class CustomerStoreHomeView(ListView):  
    model = Product
    template_name = 'customer/customer_store_view.html'
    context_object_name = 'products'

    def get_queryset(self):
        store_id = self.kwargs['store_id']
        store = get_object_or_404(Store, pk=store_id)
        return Product.objects.filter(store=store).select_related('category', 'store')

    # context에 담아 템플릿으로 전달
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store_id = self.kwargs['store_id']
        store = get_object_or_404(Store, pk=store_id)
        products = self.get_queryset()
        categories = list(set(product.category for product in products if product.category))
        context['store'] = store  # Store 정보를 컨텍스트에 추가
        context['categories'] = categories  # 중복 없는 카테고리 목록을 컨텍스트에 추가
        
        # 할인된 가격 계산 및 컨텍스트에 추가
        products_with_discount = []
        for product in products:
            discounted_price = product.product_price * (1 - product.product_sale / 100)  # 할인율을 적용한 금액
            products_with_discount.append((product, discounted_price))  
        
        context.update({
            'store': store,
            'categories': categories,
            'products_with_discount': products_with_discount,  # products_with_discount로 전달
        })
        return context