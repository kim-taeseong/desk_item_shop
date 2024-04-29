<<<<<<< HEAD
# Create your views here.
=======
>>>>>>> origin/anjiyoo
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.db.models.query import QuerySet
from .models import Product, Category
from django.views.generic import *
from django.urls import reverse_lazy
from typing import Any
<<<<<<< HEAD
from django.db.models.query import QuerySet

#-- 카테고리
# 카테고리 목록
class CategoryListView(ListView):
    model = Category
    template_name = 'category/list.html'  # 목록을 표시할 템플릿 파일

# 추가 
class CategoryCreateView(CreateView):
    model = Category
    fields = ['category_name']
    template_name = 'category/create.html'
    success_url = reverse_lazy('logistics:category_list')  

# 수정
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['category_name']
    success_url = reverse_lazy('category_list') 

# 삭제
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('category_list')

###############################################################################

#### 상품
#-- 조회
class ProductListView(ListView):
    model = Product
    template_name = 'logistics/product_list.html'
    context_object_name = 'product'
    paginate_by = 10
    def get_queryset(self):
        return self.model.objects.all()

#-- 추가
class ProductCreateView(CreateView):
=======
# Create your views here.


class AddProductView(CreateView):
>>>>>>> origin/anjiyoo
    model = Product
    template_name = 'logistics/add_product.html' # templates url 지정 필요
    # 필드 지정
    fields = ['category', 'product_name', 'product_description', 'product_price', 'product_inventory', 'product_img', 'product_sale']
    # 상품 추가 후 리다이렉트할 URL 지정
    success_url = reverse_lazy('logistics:product_list')

<<<<<<< HEAD
# Page not found (404) - 쿼리 결과에 product가 없습니다. (수정필요) > 수정완료했습니다 product_detail.html
class ProductUpdateView(UpdateView):
=======
class UpdateProductView(UpdateView):
>>>>>>> origin/anjiyoo
    model = Product
    template_name = 'logistics/update_product.html'
    fields = ['category', 'product_name', 'product_description', 'product_price', 'product_inventory', 'product_img', 'product_sale']
    success_url = reverse_lazy('logistics:product_list')
<<<<<<< HEAD

# Page not found (404) - 쿼리 결과에 product가 없습니다.(수정필요) > 수정완료했습니다 product_detail.html
=======
    
class ProductListView(ListView):
    model = Product
    template_name = 'logistics/product_list.html'
    context_object_name = 'product'
    paginate_by = 10
    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.all()

>>>>>>> origin/anjiyoo
class ProductDetailView(DetailView):
    model = Product
    template_name = 'logistics/product_detail.html'
    context_object_name = 'product'
    def get_queryset(self):
        return self.model.objects.all()
<<<<<<< HEAD

#-- 상품 삭제
class DeleteProductLV(ListView):
    model = Product
    template_name = 'logistics/list.html'  # 삭제할 상품 목록을 보여줄 템플릿 지정

class DeleteProductDV(DeleteView):
    model = Product 
    success_url = reverse_lazy('logistics:del_list')  # 삭제 후 리다이렉트할 URL 지정
    template_name = 'logistics/delete.html'  # 삭제할 상품 목록을 보여줄 템플릿 지정
=======
>>>>>>> origin/anjiyoo
