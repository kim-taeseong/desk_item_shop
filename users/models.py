from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True) # 이메일
    is_customer = models.BooleanField(default=False) # 구매자 계정인지
    is_store = models.BooleanField(default=False) # 스토어 계정인지
    deactivetime = models.DateTimeField(null=True, blank=True) # 비활성화한 시간

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='customer')
    cus_nickname = models.CharField(max_length=20) # 닉네임
    cus_name = models.CharField(max_length=20) # 이름
    cus_img = models.ImageField(upload_to='customer/img', null=True) # 프로필 이미지
    cus_height = models.IntegerField(null=True) # 키
    cus_weight = models.IntegerField(null=True) # 몸무게
    cus_job = models.CharField(max_length=20, null=True) # 직업
    cus_address = models.CharField(max_length=200) # 주소
    cus_zipcode = models.CharField(max_length=10) # 우편번호 - 수학적인 연산이 필요하지 않기에 CharField가 더 적절하다고 함
    cus_birth = models.DateField() # 생년월일
    cus_telnum = models.CharField(max_length=20) # 전화번호
    cus_regdate = models.DateTimeField(auto_now_add=True) # 가입일 자동생성

    def __str__(self) -> str:
        return self.cus_name

class Store(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, related_name='store')
    store_name = models.CharField(max_length=20) # 상호명
    store_img = models.ImageField(upload_to='store/img', null=True) # 스토어 이미지
    store_num = models.CharField(max_length=20) # 사업자번호
    store_address = models.CharField(max_length=200) # 판매점 주소
    store_zipcode = models.CharField(max_length=10) # 판매점 우편번호 - 수학적인 연산이 필요하지 않기에 CharField가 더 적절하다고 함
    store_telnum = models.CharField(max_length=20) # 연락처
    store_regdate = models.DateTimeField(auto_now_add=True) # 가입일 자동생성

    def __str__(self) -> str:
        return self.store_name
