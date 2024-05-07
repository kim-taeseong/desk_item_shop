from django.db import models
from logistics.models import Product
from users.models import Customer

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.IntegerField()
    price = models.IntegerField()
    address = models.CharField(max_length=100)