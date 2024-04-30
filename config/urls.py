from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logistics/', include('logistics.urls')),  # logistics 앱의 URL을 포함합니다.
    path('users/', include('users.urls')), 
    path('orders/', include('orders.urls')),
]
