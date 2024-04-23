from django.contrib.auth.models import AbstractUser
from django.db import models

class Store(AbstractUser):
    name = models.CharField(max_length=20)
    img = models.ImageField(upload_to='img') #imagefield
    num = models.CharField(max_length=20) # 사업자번호 유효성검사 있으면 좋을듯
    address = models.CharField(max_length=30) # 주소검색 api를 통해서 입력받으면 좋을텐데 어려우면 패스
    zipcode = models.IntegerField()
    email = models.EmailField(max_length=30) #emailfield
    telnum = models.CharField(max_length=20) # 000-0000-0000 폰번호 양식 유효성검사 있으면 좋을듯
    regdate = models.DateField(auto_now_add=True)