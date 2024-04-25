from django.urls import path
from .views import AddProductView, ProductListView,ProductDetailView

urlpatterns = [
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('product_detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'),
]
