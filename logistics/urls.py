from django.urls import path
from .views import AddProductView,ProductListView, UpdateProductView, ProductDetailView
from .views import DeleteProductDV, DeleteProductLV
from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

app_name  = 'logistics'
urlpatterns = [
    
    #카테고리
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),


    path('product/add/', AddProductView.as_view(), name='add_product'),
    path('product/list/', ProductListView.as_view(), name='product_list'),

    # Page not found (404) - 쿼리 결과에 product가 없습니다. 
    path('product/update/<int:pk>', UpdateProductView.as_view(), name='update_product'), # (수정필요)
    path('product/detail/<int:pk>', ProductDetailView.as_view(), name='product_detail'), # (수정필요)

    # 삭제
    path('product/delete/', DeleteProductLV.as_view(), name='del_list'),
    path('product/delete/<int:pk>/', DeleteProductDV.as_view(), name='del_product'),
    
]