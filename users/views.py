from django.shortcuts import redirect, render
from django.views.generic import CreateView, TemplateView
from .models import User
from logistics.models import Product
from .forms import CustomerSignUpForm, StoreSignUpForm, LoginForm
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import customer_required, store_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import views as auth_views

User = get_user_model()

class CustomerSignUpView(CreateView): # 구매자 회원가입
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
    
class StoreSignUpView(CreateView): # 판매자 회원가입
    model = User
    form_class = StoreSignUpForm
    template_name = 'users/store_signup.html' # 판매자 회원가입 페이지로 이동

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'store'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('users:signup_done') # 회원가입 완료 페이지 필요
    
class SignUpDoneView(TemplateView):
    template_name = 'users/signup_done.html'
    
class LoginView(auth_views.LoginView): # 로그인
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
        
@login_required
@customer_required
def customer_home(request): # 구매자 메인 페이지가 개발되면 그 페이지로 연결시켜야 함
    product = Product.objects.all()
    context = {
        'products': product
    }
    return render(request, 'users/customer_home.html', context)

# store_home 원본
@login_required
@store_required
def store_home(request): # 스토어 페이지가 개발되면 그 페이지로 연결시켜야 함
    product = Product.objects.all()
    context = {
        'products': product
    }
    return render(request, 'users/store_home.html', context)

# # 지안님 확인을 위한 ProductForm
# class ProductForm(forms.ModelForm):
#     class Meta:
#         model = Product
#         fields = '__all__'

# # 지안님 확인을 위한 store_home
# @login_required
# @store_required
# def store_home(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('logistics:product_list')  # 상품 추가 성공 시 logistics:product_list로 이동
#     else:
#         form = ProductForm()
    
#     product = Product.objects.all()
#     context = {
#         'form': form,
#         'products': product
#     }
#     return render(request, 'logistics/add_product.html', context) # 로그인 완료하면 logistics/add_product로 이동

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
    
