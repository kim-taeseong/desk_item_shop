from .models import User
from logistics.models import Product
from django.shortcuts import redirect, render
from .forms import CustomerSignUpForm, StoreSignUpForm, LoginForm
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from .decorators import customer_required, store_required

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
        return redirect('users:signup_done') # 회원가입 완료 페이지 필요
    
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
            if user.is_customer: # 아이디가 고객이면 고객 메인 페이지로
                return reverse('users:customer_home')
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