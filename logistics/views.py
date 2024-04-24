from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category
from django.views.generic import *
from django.urls import reverse_lazy

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

#-- 상품 조회

#-- 상품 삭제
class DeleteProductView(DeleteView):
    model = Product
    template_name = 'logistics/delete_product.html'  
    success_url = reverse_lazy('logistics:product_list.html.html')  # 삭제 후 리다이렉트할 URL 지정

class DeleteProductLV(ListView):
    model = Product
    template_name = 'logistics/delete_list.html'  # 삭제할 상품 목록을 보여줄 템플릿 지정
