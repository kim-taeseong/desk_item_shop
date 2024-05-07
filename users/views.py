from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import *
from .models import User, Customer, Store
from logistics.models import Product, Category
from .forms import CustomerSignUpForm, StoreSignUpForm, LoginForm, CustomerEditForm, StoreEditForm
from django.contrib.auth import login, get_user_model, logout, authenticate, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .decorators import customer_required, store_required
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext as _

User = get_user_model()

# 구매자 회원가입
class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'customer/customer_signup.html' # 구매자 회원가입 페이지로 이동

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('users:signup_done')
    
# 판매자 회원가입
class StoreSignUpView(CreateView):
    model = User
    form_class = StoreSignUpForm
    template_name = 'store/store_signup.html' # 판매자 회원가입 페이지로 이동

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'store'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('users:signup_done')
    
# 회원가입 완료
class SignUpDoneView(TemplateView):
    template_name = 'users/signup_done.html'

# 로그인
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def form_invalid(self, form):
        # 비활성화된 계정으로 로그인 시도 시, 계정 삭제 안내 페이지로
        username = form.cleaned_data.get('username')
        user = User.objects.filter(username=username).first()
        if user and not user.is_active:
            return HttpResponseRedirect(reverse('users:account_delete_alert'))
        return super().form_invalid(form)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_customer: # 아이디가 고객이면 메인 페이지로
                return reverse('logistics:main')
            elif user.is_store: # 아이디가 스토어면 스토어 메인 페이지로
                return reverse('users:store_home')
        else: # 잘못 입력하면 다시
            return reverse('login') 

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('users:login')  # 로그인 화면으로 리다이렉트

@login_required
# 회원탈퇴 - 실제 삭제가 아닌 비활성화
def account_delete(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            user.is_active = False  # 탈퇴 처리(실제 삭제 대신 비활성화)
            user.save()
            logout(request)
            return redirect('users:login')  # 탈퇴 후 로그인 페이지로 리다이렉트
        else:
            messages.error(request, '비밀번호가 틀렸습니다.')
            return render(request, 'account_delete/account_delete.html')
    return render(request, 'account_delete/account_delete.html')

# 회원탈퇴 알림 페이지
def account_delete_alert(request):
    return render(request, 'account_delete/account_delete_alert.html')

# 탈퇴 취소 페이지
def account_delete_cancel(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    
    try:
            user = User.objects.get(username=username, is_active=False)
            
            if user.check_password(password):
                # 비밀번호가 일치하는 경우에만 계정을 활성화 상태로 변경
                user.is_active = True
                user.save()
                
                messages.success(request, '회원 탈퇴가 취소되었습니다. 계정이 활성화되었습니다.')
                return redirect('users:login')  # 로그인 페이지로 리다이렉트
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.') # 비밀번호가 일치하지 않으면
    except User.DoesNotExist:
        messages.error(request, '해당하는 계정을 찾을 수 없습니다.') # 아이디가 일치하지 않으면

    return render(request, 'account_delete/account_delete_cancel.html')
        
    
# 즉시 탈퇴 페이지
def account_delete_now(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.objects.get(username=username)
            
            if user.check_password(password):
                # 계정이 판매자 계정인지 확인
                if hasattr(user, 'store'):
                    # 해당 판매자가 올렸던 상품들 삭제
                    Product.objects.filter(store=user.store).delete() 
                    user.store.delete()
                # 비밀번호가 일치하는 경우에만 계정을 삭제
                user.delete()
                
                messages.success(request, '계정이 성공적으로 삭제되었습니다.')
                return redirect('users:login')  # 로그인 페이지로 리다이렉트
            else:
                messages.error(request, '비밀번호가 일치하지 않습니다.') # 비밀번호가 일치하지 않으면
        except User.DoesNotExist:
            messages.error(request, '해당하는 계정을 찾을 수 없습니다.') # 아이디가 일치하지 않으면

    return render(request, 'account_delete/account_delete_now.html')


# 구매자 홈
@login_required
@customer_required
def customer_home(request): # 구매자 메인 페이지가 개발되면 그 페이지로 연결시켜야 함
    product = Product.objects.all()
    context = {
        'products': product
    }
    return render(request, 'users/customer_home.html', context)


# 아이디 찾기
def find_username(request):
    if request.method == 'POST':
        email = request.POST['email']
        users = User.objects.filter(email=email)
        if users.exists():
            user = users.first()
            # 이메일 문구
            send_mail(
                '사이트 아이디 찾기',
                f'귀하의 아이디는 {user.username} 입니다.',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            ) 
            return render(request, 'find/find_username_done.html')  # 이메일 발송 완료시 발송 완료 페이지로 이동
        else:
            # 등록된 이메일이 아닐 경우, 에러 메시지와 함께 find_username 템플릿을 다시 렌더링
            return render(request, 'find/find_username.html', {'error': '해당 이메일로 등록된 사용자가 없습니다.'})
    else:
        # GET 요청 처리
        return render(request, 'find/find_username.html')


# 고객 회원정보 수정
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
        # POST 요청이 아니라면 CustomerEditForm이 customer 인스턴스로 초기화되어 현재 정보를 customer 정보 폼에 채움
        form = CustomerEditForm(instance=customer)
    return render(request, 'edit/edit_customer.html', {'form': form})


class EditCustomerDoneView(TemplateView):
    template_name = 'edit/edit_customer_done.html'  # 고객 회원정보수정완료 페이지

    def post(self, request):
        return HttpResponseRedirect(reverse('users:edit_customer_done'))


# 스토어 회원정보 수정
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
            return redirect('users:edit_store_done')  # 스토어 회원정보수정 완료 페이지로 리다이렉션
    else:
        # POST 요청이 아니라면 StoreEditForm이 store 인스턴스로 초기화되어 현재 정보를 store 정보 폼에 채움
        form = StoreEditForm(instance=store)
    
    return render(request, 'edit/edit_store.html', {'form': form})

class EditStoreDoneView(TemplateView):
    template_name = 'edit/edit_store_done.html' # 스토어 회원정보수정완료 페이지

    def post(self, request):
        return HttpResponseRedirect(reverse('users:edit_store_done'))


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
    return render(request, 'users/edit_password.html', {'form': form})


# store_home http://127.0.0.1:8000/users/store/
class StoreDashboardView(LoginRequiredMixin, ListView):  # 새로 등록한 상품 정렬
    model = Product
    template_name = 'users/store_home.html'  # 연결되는 templates url
    context_object_name = 'products'  # 컨텍스트 객체 이름 설정

    def get_queryset(self):
        # 로그인한 사용자의 스토어에 연결된 최근에 등록된 상품 5개를 가져옴
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'store'):
            return Product.objects.filter(store=user.store).order_by('-product_date')[:5]
        else:
            return Product.objects.none()  # 상품이 없는 경우 빈 쿼리셋 반환

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# customer 기준의 store_home
class CustomerStoreHomeView(ListView):  
    model = Product
    template_name = 'users/customer_store_view.html'  # 연결되는 templates url
    context_object_name = 'products'

    def get_queryset(self):
        store_id = self.kwargs['store_id']  # URL에서 스토어 ID를 받음
        store = get_object_or_404(Store, pk=store_id)  # 해당 스토어가 없는 경우 404 에러
        return Product.objects.filter(store=store).select_related('category', 'store')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        store_id = self.kwargs['store_id']
        store = get_object_or_404(Store, pk=store_id)  # 스토어 객체를 가져옴
        # 제품 목록을 조회하여 해당 스토어의 모든 카테고리를 가져옴
        products = self.get_queryset()
        # list로 값 전달, 중복 카테고리 제거: id를 기반으로
        categories = list(set(product.category for product in products if product.category))
        context['store'] = store  # 스토어 정보를 컨텍스트에 추가
        context['categories'] = categories  # 중복 없는 카테고리 목록을 컨텍스트에 추가
        return context
