from django.db import models
from logistics.fields import ThumbnailImageField

class Category(models.Model):
    category_name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Product(models.Model):

    # 카테고리와의 외부 키 관계
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    #store_id = models.IntegerField() # 스토어 ID
    
    product_name = models.CharField(max_length=30) # 상품명
    product_description = models.TextField('상품 설명') # 설명
    product_price = models.IntegerField() # 가격
    product_date = models.DateField(auto_now_add=True) # 상품등록일
    product_inventory = models.IntegerField() # 재고
    
    product_img = ThumbnailImageField(upload_to='photo/%Y/%m') # 상품이미지
    
    product_sale = models.IntegerField(default=0) # 할인율

    def __str__(self):
        return self.name
