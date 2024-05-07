from .models import Product, Category, Store
from django.views.generic import *
from django.urls import reverse_lazy
from typing import Any
from django.db.models.query import QuerySet
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render

#-- 카테고리
# 카테고리 목록
class CategoryListView(ListView):
    model = Category
    template_name = 'category/list.html'  # 연결되는 templates url

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

#### 상품 : 각 스토별로 등록한 상품 보임 (상품등록/수정/삭제)
#-- 조회
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'logistics/list.html'  # 연결되는 templates url (수정)
    context_object_name = 'products'

    def get_queryset(self):
        # 로그인한 사용자의 스토어에 속한 상품만 필터링
        return Product.objects.filter(store__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_store = Store.objects.filter(user=self.request.user).first()

        if user_store:
            context['store'] = user_store
            # 스토어에 등록된 모든 상품 카테고리 가져오기
            context['categories'] = Category.objects.filter(product__store=user_store).distinct()
        else:
            context['store'] = None
            context['categories'] = Category.objects.none()

        return context

#-- 추가
class AddProductView(CreateView):
    model = Product
    template_name = 'logistics/create.html'  # 연결되는 templates url (수정)
    # 필드 지정
    fields = ['category', 'product_name', 'product_description', 'product_price', 'product_inventory', 'product_img', 'product_sale']
    # 상품 추가 후 리다이렉트할 URL 지정
    success_url = reverse_lazy('logistics:product_list')

    # 각 사용자가 자신의 제품만 볼 수 있음 (수정)
    def form_valid(self, form):
        try:
            user_store = Store.objects.get(user=self.request.user)
            form.instance.store = user_store
            return super().form_valid(form)
        except Store.DoesNotExist:
            form.add_error(None, '이 사용자에 대한 스토어가 존재하지 않습니다.')  # 스토어 없음 예외 처리
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['store'] = Store.objects.get(user=self.request.user)  # 현재 스토어 정보
        return context


# Page not found (404) - 쿼리 결과에 product가 없습니다. (수정필요) > 수정완료했습니다 product_detail.html
class UpdateProductView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    template_name = 'logistics/update.html'  # 연결되는 templates url (수정)
    fields = ['category', 'product_name', 'product_description', 'product_price', 'product_inventory', 'product_img', 'product_sale']
    success_url = reverse_lazy('logistics:product_list')

    # 각 사용자가 자신의 제품만 볼 수 있음 (수정)
    def test_func(self):
        product = self.get_object()
        return self.request.user == product.store.user


# Page not found (404) - 쿼리 결과에 product가 없습니다.(수정필요) > 수정완료했습니다 product_detail.html
class ProductDetailView(DetailView):
    model = Product
    template_name = 'logistics/detail.html'  # 연결되는 templates url (수정)
    context_object_name = 'product'
    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.all()


#-- 상품 삭제
class DeleteProductLV(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'logistics/list.html'  # 연결되는 templates url (수정)

    # 각 사용자가 자신의 제품만 볼 수 있음 (수정)
    def get_queryset(self):
        return Product.objects.filter(store__user=self.request.user)

class DeleteProductDV(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product 
    success_url = reverse_lazy('logistics:del_list')  # 삭제 후 리다이렉트할 URL 지정
    template_name = 'logistics/delete.html'  # 삭제할 상품 목록을 보여줄 템플릿 지정

    # 각 사용자가 자신의 제품만 볼 수 있음 (수정)
    def test_func(self):
        product = self.get_object()
        return self.request.user == product.store.user
    

###############################################################################
#### 메인페이지
#-- 메인페이지 http://127.0.0.1:8000/
class MainListView(ListView):
    model = Product
    template_name = 'main.html'  # 연결되는 templates url
    context_object_name = 'products'

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.all()


#-- 카테고리별 상품리스트 조회
class MainProductListView(ListView):
    model = Product
    template_name = 'category/cat_products.html'  # 연결되는 templates url
    context_object_name = 'products'

    def get_queryset(self):
        # URL에서 pk를 받아옴
        pk = self.kwargs.get('pk')
        self.category = Category.objects.get(pk=pk)

        # 해당 카테고리에 속하는 상품들만 필터링
        return Product.objects.filter(category=self.category).order_by('-product_date')

    def get_context_data(self, **kwargs):
        # 기본 구현을 호출하여 context를 가져옴
        context = super().get_context_data(**kwargs)
        # context에 카테고리를 추가
        context['category'] = self.category
        return context
