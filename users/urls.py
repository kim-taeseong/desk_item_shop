from django.urls import path, include
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"), # 로그인페이지
    path("customer/", views.customer_home, name="customer_home"), # 고객 메인페이지
    path("store/", views.store_home, name="store_home"), # 스토어 메인페이지
    path("signup/customer/", views.CustomerSignUpView.as_view(), name="customer_signup"), # 고객 회원가입 페이지
    path("signup/store/", views.StoreSignUpView.as_view(), name="store_signup"), # 스토어 회원가입 페이지
    path('find_username/', views.find_username, name='find_username'), # 아이디 찾기
    path('signup/done/', views.SignUpDoneView.as_view(), name='signup_done'), # 회원가입 완료 페이지
]