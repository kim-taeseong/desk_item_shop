from django.db import models

class Order(models.Model):
    order_number = models.CharField(max_length=100)
    customer_name = models.CharField(max_length=100)
    # 다른 필요한 필드도 추가할 수 있습니다.

    def __str__(self):
        return self.order_number

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    # 다른 필요한 필드도 추가할 수 있습니다.

    def __str__(self):
        return f"{self.order.order_number} - {self.payment_method}"
