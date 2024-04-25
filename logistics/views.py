from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from .models import Product, Category
from django.views.generic import *
from django.urls import reverse_lazy
from typing import Any
# Create your views here.


class AddProductView(CreateView):
    model = Product
    template_name = 'logistics/add_product.html' # templates url 지정 필요
    # 필드 지정
    fields = ['category', 'product_name', 'product_description', 'product_price', 'product_inventory', 'product_img', 'product_sale']
    # 상품 추가 후 리다이렉트할 URL 지정
    success_url = reverse_lazy('logistics:product_list')

class UpdateProductView(UpdateView):
    model = Product
    template_name = 'logistics/update_product.html'
    fields = ['category', 'product_name', 'product_description', 'product_price', 'product_inventory', 'product_img', 'product_sale']
    success_url = reverse_lazy('logistics:product_list')
    
class ProductListView(ListView):
    model = Product
    template_name = 'logistics/product_list.html'
    context_object_name = 'product'
    paginate_by = 10
    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.all()

class ProductDetailView(DetailView):
    model = Product
    template_name = 'logistics/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return self.model.objects.all()
