from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.display_orders_history, name='display_orders'),
    path('order/<int:pk>/', views.display_order, name='display_order'),
    path('order/<int:pk>/delete/', views.delete_order, name='delete_order'),
    path('order/', views.order, name='order'),
]