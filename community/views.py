from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from .models import Community, CommunityComment, CommunityCategory
from users.models import Customer
from logistics.models import Product, Category
from .forms import PostForm, PostEditForm, CommentcreateForm, CommentEditForm, CommentDeleteForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.generic import *
from django.urls import reverse_lazy, reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

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
def post_detail(request, pk):
    # 해당 pk에 해당하는 글 가져오기
    community = get_object_or_404(Community, pk=pk)
    # 해당 글에 대한 댓글 가져오기
    comments = CommunityComment.objects.filter(community=community)
    # 댓글 폼 생성
    if request.method == 'POST':
        form = CommentcreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            # 현재 로그인된 사용자의 Customer 인스턴스를 가져와서 댓글의 작성자로 설정
            comment.customer = request.user.customer
            comment.community = community
            comment.save()
            return redirect('community:post_detail', pk=community.pk)
    else:
        form = CommentcreateForm()

    # 상품 링크 추가
    product_links = community.product.all()
    return render(request, 'post/post_detail.html', {'community': community, 'comments': comments, 'form': form, 'product_link': product_links})


# 커뮤니티 글 작성
# def create_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             # 로그인한 사용자의 고객 계정 할당
#             if hasattr(request.user, 'customer'):
#                 try:
#                     post.customer = Customer.objects.get(user=request.user)
#                     post.save()
#                     form.save_m2m()  # ManyToMany 필드 저장
#                     messages.success(request, '게시글이 성공적으로 작성되었습니다.')
#                     return redirect('community:post_detail', pk=post.pk)
#                 except Customer.DoesNotExist:
#                     messages.error(request, '고객 계정이 존재하지 않습니다.')
#             else:
#                 messages.error(request, '커뮤니티 게시글은 고객 계정으로만 작성할 수 있습니다.')
#         else:
#             messages.error(request, '폼이 유효하지 않습니다. 다시 시도해 주세요.')
#     else:
#         form = PostForm()
#     categories = Category.objects.all()
#     products = Product.objects.all()
#     return render(request, 'post/create_post.html', {'form': form, 'categories': categories, 'products': products})
  
def create_post(request):
    if hasattr(request.user, 'customer'):  # 사용자가 고객 계정을 가지고 있는지 확인
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                # 로그인한 사용자의 고객 계정 할당 (customer에서 로그인한 user와 같은 user 찾기)
                try:
                    post.customer = Customer.objects.get(user=request.user)
                    post.save()
                    return redirect('community:post_detail', pk=post.pk)  # 생성 후 이동할 페이지
                except Customer.DoesNotExist:
                    messages.error(request, '고객 계정이 존재하지 않습니다.')
                    return redirect('community:create_post')
            else:
                messages.error(request, '폼이 유효하지 않습니다. 다시 시도해 주세요.')
        else:
            form = PostForm()
        return render(request, 'post/create_post.html', {'form': form})
    else:
        # 로그인 하지않은 사용자가 글 작성 버튼을 누르면 로그인 페이지로 이동
        messages.warning(request, '커뮤니티 게시글은 고객 계정으로만 작성할 수 있습니다.')
        return redirect('users:login')  # 'login'은 로그인 페이지의 URL 이름으로 가정


# 해당 카테고리의 상품 리스트
def product_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category)
    return render(request, 'post/product_list.html', {'category': category, 'products': products})



# # 커뮤니티 글 수정
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Community, pk=pk)
    if request.method == "POST":
        form = PostEditForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            # ManyToMany 필드를 처리하기 위해 form.save_m2m()을 호출합니다.
            form.save_m2m()
            return redirect('community:post_detail', pk=post.pk)  # 수정 후 이동할 페이지
    else:
        form = PostEditForm(instance=post)
    return render(request, 'post/edit_post.html', {'form': form})


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




