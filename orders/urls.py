from django.urls import path
from . import views

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),  # 주문 생성 URL
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),  # 주문 취소 URL
]
