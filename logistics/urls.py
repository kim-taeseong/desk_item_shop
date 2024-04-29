from django.urls import path
from . import views

app_name  = 'logistics'
urlpatterns = [
    
    #카테고리
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),


    path('product/add/', views.ProductCreateView.as_view(), name='add_product'),
    path('product/list/', views.ProductListView.as_view(), name='product_list'),

    # Page not found (404) - 쿼리 결과에 product가 없습니다. > 수정했습니다
    path('product/update/<int:pk>', views.ProductUpdateView.as_view(), name='update_product'), # (수정완료 product_detail.html 부분에 url 부분을 수정)
    path('product/detail/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'), # (수정완료 product_detail.html 부분에 url 부분을 수정)

    # 삭제
    path('product/delete/', views.DeleteProductLV.as_view(), name='del_list'),
    path('product/delete/<int:pk>/', views.DeleteProductDV.as_view(), name='del_product'),
    
]