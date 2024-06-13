from django.db import models
from logistics.models import Product
from users.models import Customer

# 커뮤니티 카테고리
class CommunityCategory(models.Model):
    community_cat_name = models.CharField('카테고리명', max_length=50)

    def __str__(self):
        return self.community_cat_name


# 커뮤니티 게시글
class Community(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product, related_name='communities', blank=True)  # 여러개의 상품 가져오기
    selected_products = models.ManyToManyField(Product, related_name='selected_communities', blank=True)  # 선택된 상품 (상품링크로 연결)
    community_category = models.ForeignKey(CommunityCategory, on_delete=models.CASCADE)
    community_title = models.CharField(max_length=30)  # 게시판 제목
    community_content = models.TextField()  # 게시판 본문
    community_img = models.ImageField(upload_to='community/img') # 이미지
    community_like = models.IntegerField(default=0)  # 좋아요
    liked_by = models.ManyToManyField(Customer, related_name='liked_posts')  # 좋아요를 누른 회원
    community_shotform = models.FileField(upload_to='community/videos', null=True, blank=True) # 숏폼
    community_date = models.DateTimeField(auto_now_add=True)  # 작성일 자동생성


    def __str__(self):
        return self.community_title


# 커뮤니티 게시글 댓글
class CommunityComment(models.Model):
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    community_comment_content = models.CharField(max_length=100)  # 댓글내용
    community_comment_like = models.IntegerField(default=0)  # 좋아요
    liked_by = models.ManyToManyField(Customer, related_name='liked_comments')  # 좋아요를 누른 회원
    community_comment_date = models.DateTimeField(auto_now_add=True)  # 작성일 자동생성

    def __str__(self):
        return self.community_comment_content

