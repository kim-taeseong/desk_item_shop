from django.urls import path
from community import views
from .views import ComCategoryListView, ComCategoryCreateView, ComCategoryUpdateView, ComCategoryDeleteView, MainPostListView

app_name='community'

urlpatterns = [
    # 커뮤니티 카테고리
    path('categories/', ComCategoryListView.as_view(), name='category_list'),
    path('categories/create/', ComCategoryCreateView.as_view(), name='create_category'),
    path('categories/<int:pk>/', MainPostListView.as_view(), name='cat_post'),  # 카테고리별 게시글 조회
    path('categories/<int:pk>/update/', ComCategoryUpdateView.as_view(), name='edit_category'),
    path('categories/<int:pk>/delete/', ComCategoryDeleteView.as_view(), name='delete_category'),

    # 커뮤니티 글
    path('', views.post_list, name='post_list'),  
    path('post/create/', views.create_post, name='create_post'), 

    # 상품 연결
    path('products/categories/<int:category_id>/', views.product_list_by_category, name='product_list_by_category'),
    # 상품 검색
    path('post/search/product/', views.search_product, name='search_product'),  


    path('post/<int:pk>/', views.post_detail, name='post_detail'),  
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),  
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),  
    path('post/<int:pk>/like/', views.like_post, name='like_post'),
    path('post/<int:pk>/unlike/', views.unlike_post, name='unlike_post'),

    # 댓글
    path('comment/<int:comment_id>/like/', views.like_comment, name='like_comment'),
    path('comment/<int:comment_id>/unlike/', views.unlike_comment, name='unlike_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

]
