from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Community, CommunityComment, CommunityCategory
from users.models import Customer
from logistics.models import Product, Category
from .forms import PostForm, PostEditForm, CommentcreateForm, CommentEditForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseNotFound
from django.utils.html import escape
from django.views.generic import *
from django.urls import reverse_lazy, reverse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
import json
from django.views.decorators.http import require_POST

# 커뮤니티 카테고리 ##############################################################################

# 커뮤니티 카테고리
class ComCategoryListView(ListView):
    model = CommunityCategory
    template_name = 'category/category_list.html'  # 연결되는 templates url

# 추가 
class ComCategoryCreateView(CreateView):
    model = CommunityCategory
    fields = ['community_cat_name']
    template_name = 'category/create_category.html'
    success_url = reverse_lazy('community:create_category')  

# 수정
class ComCategoryUpdateView(UpdateView):
    model = CommunityCategory
    fields = ['community_cat_name']
    success_url = reverse_lazy('category_list') 

 # 삭제
class ComCategoryDeleteView(DeleteView):
    model = CommunityCategory
    success_url = reverse_lazy('category_list')

# 카테고리별 게시글 조회
class MainPostListView(ListView):
    model = Community
    template_name = 'category/cat_post.html'
    context_object_name = 'posts'
    paginate_by = 16  # 한 페이지에 표시할 게시글 수

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        self.community_category = get_object_or_404(CommunityCategory, pk=pk)
        return Community.objects.filter(community_category=self.community_category).order_by('-community_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['community_category'] = self.community_category
        # 카테고리 목록을 context에 추가
        context['categories'] = CommunityCategory.objects.all()
        return context



# 상품검색 ##############################################################################



# 상품 연결
def product_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'post/create_post.html', {'category': category, 'products': products})


# 상품 검색
def search_product(request):
    if request.method == 'GET' or request.method == 'POST':
        product_name = request.GET.get('product_name', '') if request.method == 'GET' else request.POST.get('product_name', '')
        product_name = product_name.strip()  # 공백 제거
        
        
        if product_name:
            # 상품명에 대해 부분 일치, 정확한 일치, 혹은 유사한 결과를 반환할 수 있도록 검색 조건 추가
            products = Product.objects.filter(Q(product_name__icontains=product_name) | Q(product_name=product_name))
            
            serialized_products = []
            for product in products:
                serialized_product = {
                    'product_id': product.id,
                    'product_img': product.product_img.url,
                    'product_name': product.product_name,
                }
                serialized_products.append(serialized_product)
            # return JsonResponse({'products': serialized_products, 'communityId': community_id}, status=200, json_dumps_params={'ensure_ascii': False})
            return JsonResponse({'products': serialized_products}, status=200, json_dumps_params={'ensure_ascii': False})
        
        else:
            return JsonResponse({'error': '상품명을 입력하세요.'}, status=400, json_dumps_params={'ensure_ascii': False})
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])



# 게시글 ##############################################################################



# 커뮤니티 글 작성
@login_required
def create_post(request):
    if request.method == 'POST':
        try:
            # 폼 데이터에서 선택된 상품 ID 가져오기
            hidden_input = request.POST.get('hiddenInput')
            # hidden_input 값이 존재하면 리스트 변환
            selected_product_ids = []

            if hidden_input:
                try:
                    selected_product_ids = json.loads(hidden_input)
                except json.JSONDecodeError:
                    return JsonResponse({'error': '잘못된 형식의 데이터입니다.'}, status=400)

            # 폼 데이터와 파일 데이터 함께 처리
            form = PostForm(request.POST, request.FILES)

            if form.is_valid():
                post = form.save(commit=False)
                post.customer = request.user.customer
                post.save()
                form.save_m2m()

                # 선택된 상품 ID들을 Community 모델의 selected_products 필드에 추가
                for product_id in selected_product_ids:
                    try:
                        product = Product.objects.get(pk=product_id)  # selected_product_ids와 product_id가 같은 객체 조회
                        post.selected_products.add(product_id)  # selected_products 필드에 추가
                    except Product.DoesNotExist:
                        return JsonResponse({'error': f'상품 ID {product_id}가 존재하지 않습니다.'}, status=400)

                return JsonResponse({'message': '게시글이 성공적으로 작성되었습니다.'})
            else:
                return JsonResponse({'error': '폼이 유효하지 않습니다.'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    else:
        form = PostForm()
        return render(request, 'post/create_post.html', {'form': form})





# 커뮤니티 글 리스트
def post_list(request):
    post_list = Community.objects.all().order_by('-community_date')  # 최신 등록한 게시글 먼저 보여주기
    paginator = Paginator(post_list, 16)  # 한 페이지에 16개의 게시글을 보여줌
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 페이지 번호가 정수가 아닌 경우, 첫 페이지를 보여줌
        posts = paginator.page(1)
    except EmptyPage:
        # 페이지가 비어 있는 경우, 마지막 페이지를 보여줌
        posts = paginator.page(paginator.num_pages)
    return render(request, 'post/post_list.html', {'posts': posts})



# 커뮤니티 글 상세
@login_required
def post_detail(request, pk):
    community = get_object_or_404(Community, pk=pk)
    comments = CommunityComment.objects.filter(community=community)

    if request.method == 'POST':
        form = CommentcreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.customer = request.user.customer
            comment.community = community
            comment.save()
            return redirect('community:post_detail', pk=community.pk)
    else:
        form = CommentcreateForm()

    # Community 모델의 selected_products 필드 값을 가져옴
    selected_products = community.selected_products.all()
    product_links = community.product.all()

    context = {
        'community': community,
        'comments': comments,
        'form': form,
        'selected_products': selected_products,
    }

    return render(request, 'post/post_detail.html', context)



# 커뮤니티 글 수정
@login_required 
def edit_post(request, pk):
    community = get_object_or_404(Community, pk=pk)
    if request.method == 'POST':
        form = PostEditForm(request.POST, request.FILES, instance=community)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()  # 저장 후 post 객체를 저장
            form.save_m2m()  # ManyToMany 필드를 처리하기 위해 호출
            return redirect('community:post_detail', pk=post.pk)
    else:
        form = PostEditForm(instance=community)

    # Community 모델의 selected_products 필드 값을 가져옴
    selected_products = community.selected_products.all()

    context = {
        'form': form,
        'community': community,
        'selected_products': selected_products,
    }

    return render(request, 'post/edit_post.html', context)



# 커뮤니티 글 삭제
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Community, pk=pk)
    
    # 로그인한 사용자와 글 작성자가 같은지 확인
    if post.customer != request.user.customer:
        # 권한이 없는 사용자에게 에러 메시지를 반환하거나 다른 처리를 수행
        return HttpResponse("이 게시물을 삭제할 수 있는 권한이 없습니다.")
    
    # POST 요청을 받으면 게시물을 삭제하고 성공 메시지를 표시
    if request.method == 'POST':
        post.delete()
        return redirect('community:post_list')  # 삭제 후 이동할 페이지
    
    # GET 요청을 받으면 확인 페이지를 표시
    return render(request, 'post/delete_post.html', {'post': post})


# 게시글 좋아요 ##############################################################################


# 게시글 좋아요
@login_required
def like_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Community, pk=pk)
        if request.user.customer:  # 사용자가 고객 계정인 경우
            customer = Customer.objects.get(user=request.user)
            if customer not in post.liked_by.all():
                post.liked_by.add(customer)
                post.community_like += 1
                post.save()
        return redirect('community:post_detail', pk=pk)
    return redirect('community:post_detail', pk=pk)



# 게시글 좋아요 취소
@login_required
def unlike_post(request, pk):
    if request.method == 'POST':
        post = get_object_or_404(Community, pk=pk)
        if request.user.customer:  # 사용자가 고객 계정인 경우
            customer = Customer.objects.get(user=request.user)
            if customer in post.liked_by.all():
                post.liked_by.remove(customer)
                post.community_like -= 1
                post.save()
        return redirect('community:post_detail', pk=pk)
    return redirect('community:post_detail', pk=pk)



# 댓글 ##############################################################################



# 댓글 수정
def edit_comment(request, comment_id):
    comment = get_object_or_404(CommunityComment, id=comment_id)
    
    if request.method == 'POST':
        form = CommentEditForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('community:post_detail', pk=comment.community.pk)  # 수정 후 이동할 페이지
    else:
        form = CommentEditForm(instance=comment)
    
    return render(request, 'comment/edit_comment.html', {'form': form})



# 댓글 삭제
def delete_comment(request, comment_id):  
    comment = get_object_or_404(CommunityComment, id=comment_id)
    
    if request.method == 'POST':
        # 삭제
        comment.delete()
        return redirect('community:post_detail', pk=comment.community.pk)  # 삭제 후 이동할 페이지
    
    return render(request, 'comment/delete_comment.html', {'comment': comment})



# 댓글 좋아요
@login_required
def like_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(CommunityComment, id=comment_id)
        if request.user.customer:  # 사용자가 고객 계정인 경우
            customer = Customer.objects.get(user=request.user)
            if customer not in comment.liked_by.all():
                comment.liked_by.add(customer)
                comment.community_comment_like += 1
                comment.save()
        return redirect('community:post_detail', pk=comment.community.pk)
    return redirect('community:post_detail', pk=comment.community.pk)



# 댓글 좋아요 취소
@login_required
def unlike_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(CommunityComment, id=comment_id)
        if request.user.customer:  # 사용자가 고객 계정인 경우
            customer = Customer.objects.get(user=request.user)
            if customer in comment.liked_by.all():
                comment.liked_by.remove(customer)
                comment.community_comment_like -= 1
                comment.save()
        return redirect('community:post_detail', pk=comment.community.pk)
    return redirect('community:post_detail', pk=comment.community.pk)




