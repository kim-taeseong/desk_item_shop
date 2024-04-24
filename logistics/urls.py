from django.urls import path
from .views import AddProductView,ProductListView

app_name  = 'logistics'
urlpatterns = [
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
]