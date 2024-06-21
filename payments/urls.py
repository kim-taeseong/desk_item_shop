# payments/urls.py

from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('create-order/<int:product_id>/', views.create_order, name='create_order'),
    path('process-payment/<int:order_id>/', views.process_payment, name='process_payment'),
    path('success/', views.success, name='success'),
    path('error/', views.error, name='error'),
    path('verify-payment/<int:payment_id>/', views.verify_payment, name='verify_payment'),
    path('cancel-payment/<int:payment_id>/', views.cancel_payment, name='cancel_payment'),
    path('callback/', views.callback, name='callback'),
]
