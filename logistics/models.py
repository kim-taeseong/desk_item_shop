from django.db import models
from  logistics.fields import ThumbnailImageField

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100) #상품명
    description = models.TextField() # 설명
    price = models.DecimalField(max_digits=10, decimal_places=2) #가격
    created_at = models.DateTimeField(auto_now_add=True) #등록일
    stock = models.IntegerField() #재고
    image = ThumbnailImageField(upload_to='product_images/')  # 이미지를 product_images/ 폴더에 업로드합니다.
    discount_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0) #할인율

    def __str__(self):
        return self.name

