from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('logistics/',include('logistics.urls')),
<<<<<<< HEAD
=======
    path('cart/',include('cart.urls')),
>>>>>>> origin/anjiyoo
    path("", include("users.urls")),
]
