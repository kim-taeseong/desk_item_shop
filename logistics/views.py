from .models import Product, Category
from django.views.generic import *
from django.urls import reverse_lazy
from typing import Any
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
    template_name = 'logistics/list.html'
    context_object_name = 'product'
    paginate_by = 10
    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.all()

#-- 추가
class AddProductView(CreateView):
    model = Product
    template_name = 'logistics/add.html'
    # 필드 지정
    fields = ['category', 'product_name', 'product_description', 'product_price', 'product_inventory', 'product_img', 'product_sale']
    # 상품 추가 후 리다이렉트할 URL 지정
    success_url = reverse_lazy('logistics:product_list')

# Page not found (404) - 쿼리 결과에 product가 없습니다. (수정필요) > 수정완료했습니다 product_detail.html
class UpdateProductView(UpdateView):
    model = Product
    template_name = 'logistics/update.html'
    fields = ['category', 'product_name', 'product_description', 'product_price', 'product_inventory', 'product_img', 'product_sale']
    success_url = reverse_lazy('logistics:product_list')

# Page not found (404) - 쿼리 결과에 product가 없습니다.(수정필요) > 수정완료했습니다 product_detail.html
class ProductDetailView(DetailView):
    model = Product
    template_name = 'logistics/product_detail.html'
    context_object_name = 'product'
    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.all()

#-- 상품 삭제
class DeleteProductLV(ListView):
    model = Product
    template_name = 'logistics/list.html'  # 삭제할 상품 목록을 보여줄 템플릿 지정

class DeleteProductDV(DeleteView):
    model = Product 
    success_url = reverse_lazy('logistics:del_list')  # 삭제 후 리다이렉트할 URL 지정
    template_name = 'logistics/delete.html'  # 삭제할 상품 목록을 보여줄 템플릿 지정
