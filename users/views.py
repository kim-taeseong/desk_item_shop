from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, get_user_model, logout
from django.views.generic import *
from .models import User, Customer, Store
from logistics.models import Product
from .forms import CustomerSignUpForm, StoreSignUpForm, LoginForm, CustomerEditForm, StoreEditForm
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .decorators import customer_required, store_required
from django import forms
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages

User = get_user_model()

# 구매자 회원가입
class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/customer_signup.html' # 구매자 회원가입 페이지로 이동

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
    template_name = 'users/store_signup.html' # 판매자 회원가입 페이지로 이동

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

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user # 아이디가 고객인지 스토어인지
        if user.is_authenticated:
            if user.is_customer: # 아이디가 고객이면 메인 페이지로
                return reverse('logistics:main')
            elif user.is_store: # 아이디가 스토어면 스토어 메인 페이지로
                return reverse('users:store_home')
        else:
            return reverse('login') # 잘못 입력하면 다시
        
# customer_home
@login_required
@customer_required
def customer_home(request): # 구매자 메인 페이지가 개발되면 그 페이지로 연결시켜야 함
    product = Product.objects.all()
    context = {
        'products': product
    }
    return render(request, 'users/customer_home.html', context)

# store_home
@login_required
@store_required
def store_home(request): # 스토어 페이지가 개발되면 그 페이지로 연결시켜야 함
    product = Product.objects.all()
    context = {
        'products': product
    }
    return render(request, 'users/store_home.html', context)

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
            return render(request, 'users/find_username_done.html')  # 이메일 발송 완료시 발송 완료 페이지로 이동
        else:
            # 등록된 이메일이 아닐 경우, 에러 메시지와 함께 find_username 템플릿을 다시 렌더링
            return render(request, 'users/find_username.html', {'error': '해당 이메일로 등록된 사용자가 없습니다.'})
    else:
        # GET 요청 처리
        return render(request, 'users/find_username.html')
    
# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('users:login')  # 로그인 화면으로 리다이렉트


# 고객 회원정보 수정
@login_required
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
    return render(request, 'users/edit_customer.html', {'form': form})


class EditCustomerDoneView(TemplateView):
    template_name = 'users/edit_customer_done.html'  # 고객 회원정보수정완료 페이지

    def post(self, request):
        return HttpResponseRedirect(reverse('users:edit_customer_done'))


# 스토어 회원정보 수정
@login_required
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
    
    return render(request, 'users/edit_store.html', {'form': form})

class EditStoreDoneView(TemplateView):
    template_name = 'users/edit_store_done.html' # 스토어 회원정보수정완료 페이지

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
