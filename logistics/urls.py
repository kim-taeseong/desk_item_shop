from django.urls import path
from logistics import views

app_name = 'logistics'
urlpatterns = [
    # Example: /logistics/
    path('', views.CategoryLV.as_view(), name='index'),

    # Example: /logistics/category/ 
    path('category/', views.CategoryLV.as_view(), name='category'),
]
