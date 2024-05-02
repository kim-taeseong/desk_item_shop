from django.db import models
from logistics.fields import ThumbnailImageField
from django.urls import reverse
from users.models import *  # 유저 모델 참조

class Category(models.Model):
    category_name = models.CharField('카테고리명', max_length=50)

    def __str__(self):
        return self.category_name
    
    # 카테고리의 pk를 사용하여 URL 생성
    def get_absolute_url(self):
        return reverse('logistics:product_detail', args=(self.pk, ))

class Product(models.Model):
    # 카테고리와의 외부 키 관계
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # 스토어와의 외부 키 관계 (추가)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    
    product_name = models.CharField(verbose_name='상품명', max_length=30) # 상품명
    product_description = models.TextField('상품 설명') # 설명
    product_price = models.IntegerField(verbose_name='가격') # 가격
    product_date = models.DateField('등록일', auto_now_add=True) # 상품등록일
    product_inventory = models.IntegerField(verbose_name='재고') # 재고
    
    product_img = ThumbnailImageField(upload_to='photo/%Y/%m',verbose_name='이미지') # 상품이미지
    
    product_sale = models.IntegerField(default=0,verbose_name='할인율') # 할인율

    # 메타데이터 설정
    class Meta:

        # 정렬 순서
        ordering=('-product_date',)

    def __str__(self):
        return self.product_name

    # 상품의 pk를 사용하여 URL 생성
    def get_absolute_url(self):
        return reverse('logistics:product_detail', args=(self.pk, ))