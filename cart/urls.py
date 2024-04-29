from django.urls import path
from .views import CartView

app_name = 'cart'
urlpatterns = [
    path('cart_detail/<int:cart_id>/', CartView.as_view(), name='cart_detail'),
]