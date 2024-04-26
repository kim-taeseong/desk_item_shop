from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import User, Customer, Store
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomerSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(),label='이메일')
    password1 = forms.CharField(widget=forms.PasswordInput(),label='비밀번호')
    password2 = forms.CharField(widget=forms.PasswordInput(),label='비밀번호 확인')

    cus_nickname = forms.CharField(widget=forms.TextInput(),label='닉네임')
    cus_name = forms.CharField(widget=forms.TextInput(),label='이름')
    cus_img = forms.ImageField(label='프로필 이미지')
    cus_height = forms.IntegerField(widget=forms.NumberInput(),label='키')
    cus_weight = forms.IntegerField(widget=forms.NumberInput(),label='몸무게')
    cus_job = forms.CharField(widget=forms.TextInput(),label='직업')
    cus_address = forms.CharField(widget=forms.TextInput(),label='주소')
    cus_zipcode = forms.CharField(widget=forms.TextInput(),label='우편번호')
    cus_birth = forms.DateField(widget=forms.DateInput(),label='생년월일')
    cus_telnum = forms.CharField(widget=forms.TextInput(),label='전화번호')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2','cus_nickname','cus_name','cus_img','cus_height','cus_weight','cus_job',
                  'cus_address','cus_zipcode','cus_birth','cus_telnum')
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True
        if commit:
            user.save()
        customer = Customer.objects.create(
            user=user, 
            cus_nickname=self.cleaned_data.get('cus_nickname'), 
            cus_name=self.cleaned_data.get('cus_name'), 
            cus_img=self.cleaned_data.get('cus_img'),
            cus_height=self.cleaned_data.get('cus_height'),
            cus_weight=self.cleaned_data.get('cus_weight'),
            cus_job=self.cleaned_data.get('cus_job'),
            cus_address=self.cleaned_data.get('cus_address'),
            cus_zipcode=self.cleaned_data.get('cus_zipcode'),
            cus_birth=self.cleaned_data.get('cus_birth'),
            cus_telnum=self.cleaned_data.get('cus_telnum'),
        )
        return user
    

class StoreSignUpForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(),label='이메일')
    password1 = forms.CharField(widget=forms.PasswordInput(),label='비밀번호')
    password2 = forms.CharField(widget=forms.PasswordInput(),label='비밀번호 확인')

    # Store 모델에 맞춰 필드 추가
    store_name = forms.CharField(max_length=20, widget=forms.TextInput(),label='상호명')
    store_img = forms.ImageField(label='스토어 이미지')
    store_num = forms.CharField(max_length=20, widget=forms.TextInput(),label='사업자 번호')
    store_address = forms.CharField(max_length=200, widget=forms.TextInput(),label='판매자 주소')
    store_zipcode = forms.CharField(max_length=10, widget=forms.TextInput(),label='판매자 우편번호')
    store_telnum = forms.CharField(max_length=20, widget=forms.TextInput(),label='가입일')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'store_name','store_img' ,'store_num', 'store_address', 'store_zipcode',
                   'store_telnum')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_store = True  # 사용자에게 is_store 플래그 설정
        if commit:
            user.save()

        store = Store.objects.create(user=user, 
                                     store_name=self.cleaned_data.get('store_name'), 
                                     store_img=self.cleaned_data.get('store_img'),
                                     store_num=self.cleaned_data.get('store_num'), 
                                     store_address=self.cleaned_data.get('store_address'), 
                                     store_zipcode=self.cleaned_data.get('store_zipcode'), 
                                     store_telnum=self.cleaned_data.get('store_telnum'))
        return user
    
class LoginForm(AuthenticationForm):
    email = forms.EmailField(widget=forms.EmailInput(), label='이메일')
    password = forms.CharField(widget=forms.PasswordInput(),label='비밀번호')

