from django.urls import path
from . import views

urlpatterns = [
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('purchase/', views.purchase, name='purchase'),
    # 기타 필요한 URL 패턴들을 추가할 수 있음
]
