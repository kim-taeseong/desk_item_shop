from django.db import models

# 주문자 정보를 저장하는 모델
class Customer(models.Model):
    name = models.CharField(max_length=100)  # 주문자의 이름
    email = models.EmailField()  # 주문자의 이메일
    phone_number = models.CharField(max_length=15)  # 주문자의 전화번호

# 배송지 정보를 저장하는 모델
class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # 주문자와의 관계
    address = models.TextField()  # 배송지 주소
    postal_code = models.CharField(max_length=10)  # 우편번호
    # 추가 필드는 필요에 따라 추가할 수 있습니다.

# 상품 정보를 저장하는 모델
class Product(models.Model):
    name = models.CharField(max_length=100)  # 상품명
    price = models.DecimalField(max_digits=10, decimal_places=2)  # 상품 가격
    # 추가 필드는 필요에 따라 추가할 수 있습니다.

# 주문 정보를 저장하는 모델
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # 주문자와의 관계
    shipping_address = models.ForeignKey(ShippingAddress, on_delete=models.CASCADE)  # 배송지와의 관계
    products = models.ManyToManyField(Product, through='OrderItem')  # 주문 상품과의 관계
    # 추가 필드는 필요에 따라 추가할 수 있습니다.

# 주문 상품 정보를 저장하는 모델 (주문과 상품 사이의 중간 모델)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)  # 주문과의 관계
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # 상품과의 관계
    quantity = models.IntegerField()  # 주문 수량
