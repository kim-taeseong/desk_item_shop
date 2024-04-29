from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"), # 로그인페이지
    path("customer/", views.customer_home, name="customer_home"), # 고객 메인페이지
    path("store/", views.store_home, name="store_home"), # 스토어 메인페이지
    path("signup/customer/", views.CustomerSignUpView.as_view(), name="customer_signup"), # 고객 회원가입 페이지
    path("signup/store/", views.StoreSignUpView.as_view(), name="store_signup"), # 스토어 회원가입 페이지
    path('find_username/', views.find_username, name='find_username'), # 아이디 찾기
    path('signup/done/', views.SignUpDoneView.as_view(), name='signup_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
