from django.urls import path
from .views import AddProductView, ProductListView 
from .views import DeleteProductDV, DeleteProductLV
from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

app_name  = 'logistics'
urlpatterns = [
    
    #카테고리
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/create/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),

    path('add_product/', AddProductView.as_view(), name='add_product'),

    # 삭제
    path('del/', DeleteProductLV.as_view(), name='del_list'),
    path('del/<int:pk>/', DeleteProductDV.as_view(), name='del_product'),
    
]