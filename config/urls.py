"""
URL configuration for project_config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
