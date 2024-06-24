
from django.urls import path
from .views import AddProductView,ProductListView, UpdateProductView, ProductDetailView
from .views import DeleteProductDV, DeleteProductLV
from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
from .views import MainListView, MainProductListView
from . import views

app_name  = 'logistics'
urlpatterns = [

    path('product/add/', AddProductView.as_view(), name='add_product'),
    path('product/list/', ProductListView.as_view(), name='product_list'),


    path('product/update/<int:pk>', UpdateProductView.as_view(), name='update_product'), 
    path('product/detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'), 

    # 삭제
    path('product/delete/', DeleteProductLV.as_view(), name='del_list'),
    path('product/delete/<int:pk>/', DeleteProductDV.as_view(), name='del_product'),

    # customer 메인 페이지 : 카테고리별 상품리스트 조회
    path('', MainListView.as_view(), name='main'),
    path('categories/<int:pk>/', MainProductListView.as_view(), name='cat_products'),

    path('product/<int:product_id>/add_review/', views.add_review, name='add_review'),
    path('product/reviews/<int:product_id>/', views.review_detail, name='review_detail'),
]
