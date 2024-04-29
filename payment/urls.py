from django.urls import path
from .views import create_order, process_payment

urlpatterns = [
    path('create_order/', create_order, name='create_order'),
    path('process_payment/', process_payment, name='process_payment'),
]
