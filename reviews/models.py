from django.db import models
from users.models import Customer
from logistics.models import Product
from django.core.validators import MaxValueValidator, MinValueValidator

class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='reviews/', null=True, blank=True)
    rate = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    content = models.TextField(max_length=500)  # 더 길게 작성할 수 있도록 TextField로 변경
    review_date = models.DateTimeField(auto_now_add=True)  # 작성일 자동생성

    def __str__(self):
        return f'{self.customer} - {self.product} ({self.rate})'
