from django.urls import path
from .views import add_to_cart, cart_detail, remove_from_cart, update_cart_item

app_name = 'cart'

urlpatterns = [
    path('add/<int:item_id>/', add_to_cart, name='add_to_cart'),
    path('', cart_detail, name='cart_detail'),
    path('remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('update-cart-item/', update_cart_item, name='update_cart_item'),

]
