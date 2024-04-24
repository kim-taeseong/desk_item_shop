from django.urls import path
from .views import AddProductView, ProductListView 
from .views import DeleteProductView, DeleteProductLV

app_name  = 'logistics'
urlpatterns = [

    path('add_product/', AddProductView.as_view(), name='add_product'),

    path('delete_product/<int:pk>/', DeleteProductView.as_view(), name='delete_product'),
    path('delete_list/', DeleteProductLV.as_view(), name='delete_list'),
    
    path('product_list/', ProductListView.as_view(), name='product_list'),
]