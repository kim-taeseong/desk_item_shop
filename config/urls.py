from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('logistics/',include('logistics.urls')),
=======
    path('logistics/', include('logistics.urls'))
>>>>>>> bfafe79308daeb42c921a78aa903aa011f7aa52e
]
