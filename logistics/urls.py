from django.urls import path
from .views import AddProductView,ProductListView,UpdateProductView, ProductDetailView

app_name = 'logistics'
urlpatterns = [
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('update_product/<int:pk>', UpdateProductView.as_view(), name='update_product'),
    path('product_detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
]