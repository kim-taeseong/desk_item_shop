from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from django.views.generic import *
from django.urls import reverse_lazy
# Create your views here.


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