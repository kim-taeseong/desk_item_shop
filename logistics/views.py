from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from django.views.generic import *
from django.urls import reverse_lazy

#-- 카테고리
# 카테고리 목록
class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'  # 카테고리 목록을 표시할 템플릿 파일

# 카테고리 추가 후 리다이렉트할 URL
class CategoryCreateView(CreateView):
    model = Category
    fields = ['category_name']
    template_name = 'category/category_create.html'
    success_url = reverse_lazy('logistics:category_list')  

# 카테고리 수정 후 리다이렉트할 URL
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['category_name']
    success_url = reverse_lazy('category_list') 

 # 카테고리 삭제 후 리다이렉트할 URL
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')


#-- 상품 리스트
class ProductLV(ListView):
    model = Product
    template_name = 'logistics/list.html'

class ProductDV(DetailView):
    model = Product


#-- 상품 추가
class AddProductView(CreateView):
    model = Product
    template_name = 'logistics/add_product.html' # templates url 지정 필요
    # 필드 지정
    fields = ['category_id', 'product_name', 'product_description', 'product_price', 'product_inventory', 'product_img', 'product_sale']
    
    # 상품 추가 후 리다이렉트할 URL 지정
    success_url = reverse_lazy('product_list')
    
class ProductListView(ListView):
    model = Product
    template_name = 'logistics/product_list.html'


#-- 상품 삭제
class DeleteProductLV(ListView):
    model = Product
    template_name = 'logistics/del_list.html'  # 삭제할 상품 목록을 보여줄 템플릿 지정

class DeleteProductDV(DeleteView):
    model = Product 
    success_url = reverse_lazy('logistics:del_list')  # 삭제 후 리다이렉트할 URL 지정
    template_name = 'logistics/del_product.html'  # 삭제할 상품 목록을 보여줄 템플릿 지정


#-- 상품 조회