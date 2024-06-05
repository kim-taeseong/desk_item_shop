from django import forms
from django.utils.safestring import mark_safe
from .models import Community, CommunityComment, CommunityCategory
from logistics.models import Product, Category

# 게시글 작성
class PostForm(forms.ModelForm):
    # 게시글 카테고리 필드
    community_category = forms.ModelChoiceField(
        queryset=CommunityCategory.objects.all(),  
        required=False,
        label="게시글 카테고리"
    )

    # 상품 카테고리 필드
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="상품 카테고리"
    )

    class Meta:
        model = Community
        fields = ['community_category', 'community_title', 'community_img', 'community_content', 'category'] 
        labels = {
            'community_category': '게시글 카테고리', 
            'community_title': '제목',  
            'community_img': '이미지',
            'community_content': '내용',
            'category': '상품 카테고리',
        }

    
# 게시글 수정
class PostEditForm(forms.ModelForm):
    # 게시글 카테고리 필드
    community_category = forms.ModelChoiceField(
        queryset=CommunityCategory.objects.all(),  
        required=False,
        label="게시글 카테고리"
    )

    # 상품 카테고리 필드
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="상품 카테고리"
    )

    class Meta:
        model = Community
        fields = ['community_category', 'community_title', 'community_img', 'community_content', 'category'] 
        labels = {
            'community_category': '게시글 카테고리', 
            'community_title': '제목',  
            'community_img': '이미지',
            'community_content': '내용',
            'category': '상품 카테고리',
        }


# 댓글 작성
class CommentcreateForm(forms.ModelForm):
    class Meta:
        model = CommunityComment
        fields = ['community_comment_content']
        labels = {
            'community_comment_content': '댓글',  
        }

# 댓글 수정
class CommentEditForm(forms.ModelForm):
    class Meta:
        model = CommunityComment
        fields = ['community_comment_content']
        labels = {
            'community_comment_content': '수정',  
        }

# 댓글 삭제
class CommentDeleteForm(forms.ModelForm):
    class Meta:
        model = CommunityComment
        fields = []
