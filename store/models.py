from django.contrib.auth.models import AbstractUser
from django.db import models

class Store(AbstractUser): 
    # AbstractUser에서 기본적으로 제공하는 필드가 있음 따라서 실제 화면에서는 fields = [] 를 이용해 어떤 필드만 표시할건지 결정 가능
    store_name = models.CharField(max_length=30) # 상호명
    store_img = models.ImageField(upload_to='img') # 스토어 이미지
    num = models.CharField(max_length=20) # 사업자번호 [유효성 검사 있으면 좋을듯]
    address = models.CharField(max_length=30) # 회사 주소 [주소검색 api를 통해서 입력받으면 좋을텐데 어려우면 패스]
    zipcode = models.IntegerField() # 회사 우편번호
    email = models.EmailField(max_length=30) # 이메일
    telnum = models.CharField(max_length=20) # 연락처 폰번호 양식 유효성검사 있으면 좋을듯
    regdate = models.DateField(auto_now_add=True) # 가입일
    # 비밀번호는 기본으로 제공됨
    # username도 기본으로 제공된다는데 확인 필요

    def __str__(self):
        return self.name