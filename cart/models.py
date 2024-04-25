from django.db import models
from logistics.models import Product

# Create your models here.
class Cart(models.Model):
    # 기본 id
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # 상품
    # user = models.ForeignKey(User, on_delete=models.CASCADE) # 구매자 
    amount = models.IntegerField(default=0) # 수량
    
    def __str__(self):
        return self.product.product_name