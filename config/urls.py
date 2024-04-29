from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logistics/',include('logistics.urls')),
    path("", include("users.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    # 비밀번호 초기화
    path('accounts/password_reset/form', auth_views.PasswordResetView.as_view(), name="password_reset"), # 이메일 입력 화면
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"), # 이메일 발송 완료 화면
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), # 이메일 클릭 > 비밀번호 입력 화면
    path('accounts/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),  # 비밀번호 초기화 완료 화면
]
