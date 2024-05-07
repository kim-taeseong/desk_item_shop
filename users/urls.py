from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeDoneView  # Django 제공 view
from .views import *

app_name = 'users'

urlpatterns = [
    # 로그인페이지
    path("", views.LoginView.as_view(), name="login"),
    # 스토어 메인페이지
    path("store/", views.StoreDashboardView.as_view(), name="store_home"),
    # 고객 기준 스토어 페이지
    path('store/<int:store_id>/', views.CustomerStoreHomeView.as_view(), name='cus_store_home'),
    # 고객 마이페이지
    path('customer/', views.customer_home, name='customer_home'),
    # 고객 기준 스토어 페이지 - 카테고리
    path('store/<int:store_id>/category/<int:category_id>/', views.CustomerStoreHomeView.as_view(), name='cus_store_home_cat'),
    # 고객 회원가입 페이지
    path("signup/customer/", views.CustomerSignUpView.as_view(), name="customer_signup"),
    # 스토어 회원가입 페이지
    path("signup/store/", views.StoreSignUpView.as_view(), name="store_signup"),
    # 아이디 찾기
    path('find_username/', views.find_username, name='find_username'),
    # 회원가입 완료 페이지
    path('signup/done/', views.SignUpDoneView.as_view(), name='signup_done'),
    # 로그아웃
    path('logout/', views.logout_view, name='logout'),
    # 고객 회원정보 수정 페이지
    path('edit/customer/', views.edit_customer, name='edit_customer'),
    # 고객 회원정보 수정 완료 페이지
    path('edit/customer/done/', views.EditCustomerDoneView.as_view(), name='edit_customer_done'),
    # 스토어 회원정보 수정 페이지
    path('edit/store/', views.edit_store, name='edit_store'),
    # 스토어 회원정보 수정 완료 페이지
    path('edit/store/done/', views.EditStoreDoneView.as_view(), name='edit_store_done'),
    # 비밀번호 변경 페이지
    path('edit/password/', views.edit_password, name='edit_password'),
    # 비밀번호 변경 완료 페이지
    path('edit/password/done/', PasswordChangeDoneView.as_view(template_name='users/edit_password_done.html'), name='edit_password_done'),
    # 회원탈퇴
    path('account/delete/', views.account_delete, name='account_delete'),
    # 회원탈퇴 안내 페이지
    path('account_delete_alert/', views.account_delete_alert, name='account_delete_alert'),
    # 탈퇴 취소
    path('account/delete/cancel', views.account_delete_cancel, name='account_delete_cancel'),
    # 즉시 탈퇴
    path('account/delete/now', views.account_delete_now, name='account_delete_now'),
]
