from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/',include('users.urls')),
    path("", include("logistics.urls")),
    path('orders/', include('order.urls')),
    path("inquiry/", include("inquiry.urls")),
    path('cart/', include('cart.urls')),
    # 비밀번호 초기화
    path('accounts/password_reset/form', auth_views.PasswordResetView.as_view(), name="password_reset"), # 이메일 입력 화면
    path('accounts/password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"), # 이메일 발송 완료 화면
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'), # 이메일 클릭 > 비밀번호 입력 화면
    path('accounts/password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),  # 비밀번호 초기화 완료 화면
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)