from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.db import transaction
from .models import User, Customer, Store
from django import forms
from django.contrib.auth import get_user_model
import re
from django.core.exceptions import ValidationError
from django.forms.widgets import DateInput
from django.utils.translation import gettext as _

User = get_user_model() # models.py에서 User 모델을 가져옴

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8 or len(password) > 12:
            raise ValidationError(_('비밀번호는 8자 이상 12자 이하여야 합니다.'))
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('비밀번호는 적어도 하나의 숫자를 포함해야 합니다.'))
        if not any(char.isupper() for char in password):
            raise ValidationError(_('비밀번호는 적어도 하나의 대문자를 포함해야 합니다.'))
        if not any(char.islower() for char in password):
            raise ValidationError(_('비밀번호는 적어도 하나의 소문자를 포함해야 합니다.'))

        for i in range(len(password) - 2):
            if password[i].isdigit() and password[i+1].isdigit() and password[i+2].isdigit():
                if int(password[i+1]) == int(password[i]) + 1 and int(password[i+2]) == int(password[i]) + 2:
                    raise ValidationError(_('비밀번호는 연속되는 숫자를 포함할 수 없습니다.'))

    def get_help_text(self):
        return _('비밀번호는 8자 이상 12자 이하이며, 대문자, 소문자, 숫자를 각각 적어도 하나씩 포함해야 하며, 연속되는 숫자를 포함할 수 없습니다.')

class CustomerSignUpForm(UserCreationForm): # 구매자 계정 회원가입 폼

    def clean_username(self): # 아이디 유효성 검사
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9_]{6,16}$', username): # 조건
            raise ValidationError('아이디는 6-16자, 영문 대소문자와 "_"만 사용 가능합니다.') # 틀릴 시 메시지
        return username

    def clean_password1(self): # 비밀번호 유효성 검사
        password1 = self.cleaned_data['password1']
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,12}$', password1): # 조건
            raise ValidationError('비밀번호는 8-12자, 영문 대문자+소문자+숫자를 포함해야 합니다.') # 틀릴 시 메시지
        if re.search(r'(.)\1\1', password1): # 조건
            raise ValidationError('비밀번호에 연속되는 숫자를 포함할 수 없습니다.') # 틀릴 시 메시지
        return password1

    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@example.com'}),label='이메일')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '대소문자, 숫자 포함 8-12자'}),label='비밀번호')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 확인'}),label='비밀번호 확인')

    # Customer 모델에 맞춰 필드 추가
    cus_nickname = forms.CharField(widget=forms.TextInput(),label='닉네임')
    cus_name = forms.CharField(widget=forms.TextInput(),label='이름')
    cus_img = forms.ImageField(label='프로필 이미지')
    cus_height = forms.IntegerField(widget=forms.NumberInput(), label='키', required=False) # 키 ,무게, 직업은 필수 아님
    cus_weight = forms.IntegerField(widget=forms.NumberInput(), label='몸무게', required=False)
    cus_job = forms.CharField(widget=forms.TextInput(), label='직업', required=False)
    cus_address = forms.CharField(widget=forms.TextInput(),label='주소')
    cus_zipcode = forms.CharField(widget=forms.TextInput(),label='우편번호')
    cus_birth = forms.DateField(
        widget=DateInput(attrs={'type': 'date'}),  # DateInput 위젯 사용
        label='생년월일'
    )
    cus_telnum = forms.CharField(widget=forms.TextInput(),label='전화번호')

    def __init__(self, *args, **kwargs): # 비밀번호 입력 필드 옆 안내메시지
        super(CustomerSignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = '비밀번호는 8-12자, 영문 대문자+소문자+숫자를 포함해야 합니다. 연속되는 숫자를 포함할 수 없습니다.'
        self.fields['username'].label = '아이디'
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2','cus_nickname','cus_name','cus_img','cus_height','cus_weight','cus_job',
                  'cus_address','cus_zipcode','cus_birth','cus_telnum') # 입력받을 항목들
        help_texts = {
            'username': '아이디는 6-16자, 영문 대소문자와 "_"만 사용 가능합니다.',
            'password1': '비밀번호는 8-12자, 영문 대문자+소문자+숫자를 포함해야 합니다 . 연속되는 숫자를 포함할 수 없습니다'
        } # 필드 옆 안내메시지
    
    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = True # 로그인한 계정이 구매자임을 나타냄
        if commit: 
            user.save() # user를 저장
        customer = Customer.objects.create( # customer를 생성하고 DB에 저장 
            user=user, # 각 필드에서 입력한 값들
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
        return user # 최종적으로 생성된 구매자 객체를 반환
    

class StoreSignUpForm(UserCreationForm): # 판매자 계정 회원가입 폼

    def clean_username(self): # 아이디 유효성 검사
        username = self.cleaned_data['username']
        if not re.match(r'^[a-zA-Z0-9_]{6,16}$', username): # 조건
            raise ValidationError('아이디는 6-16자, 영문 대소문자와 "_"만 사용 가능합니다.') # 틀릴 시 메시지
        return username

    def clean_password1(self): # 비밀번호 유효성 검사
        password1 = self.cleaned_data['password1']
        if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,12}$', password1): # 조건
            raise ValidationError('비밀번호는 8-12자, 영문 대문자+소문자+숫자를 포함해야 합니다.') # 틀릴 시 메시지
        if re.search(r'(.)\1\1', password1): # 조건
            raise ValidationError('비밀번호에 연속되는 숫자를 포함할 수 없습니다.') # 틀릴 시 메시지
        return password1
    
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'example@example.com'}),label='이메일')
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '대소문자, 숫자 포함 8-12자'}),label='비밀번호')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '비밀번호 확인'}),label='비밀번호 확인')

    # Store 모델에 맞춰 필드 추가
    store_name = forms.CharField(max_length=20, widget=forms.TextInput(),label='상호명')
    store_img = forms.ImageField(label='스토어 이미지')
    store_num = forms.CharField(max_length=20, widget=forms.TextInput(),label='사업자 번호')
    store_address = forms.CharField(max_length=200, widget=forms.TextInput(),label='판매자 주소')
    store_zipcode = forms.CharField(max_length=10, widget=forms.TextInput(),label='판매자 우편번호')
    store_telnum = forms.CharField(max_length=20, widget=forms.TextInput(),label='연락처')

    def __init__(self, *args, **kwargs): # 비밀번호 입력 필드 옆 안내메시지
        super(StoreSignUpForm, self).__init__(*args, **kwargs)
        self.fields['password1'].help_text = '비밀번호는 8-12자, 영문 대문자+소문자+숫자를 포함해야 합니다. 연속되는 숫자를 포함할 수 없습니다.'
        self.fields['username'].label = '아이디'

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'store_name','store_img' ,'store_num', 'store_address', 'store_zipcode',
                   'store_telnum') # 입력받을 항목들
        help_texts = {
            'username': '아이디는 6-16자, 영문 대소문자와 "_"만 사용 가능합니다.',
            'password1': '비밀번호는 8-12자, 영문 대문자+소문자+숫자를 포함해야 합니다 . 연속되는 숫자를 포함할 수 없습니다'
        } # 필드 옆 안내메시지

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_store = True  # 로그인한 계정이 판매자임을 나타냄
        if commit:
            user.save() # user를 저장
        store = Store.objects.create( # customer를 생성하고 DB에 저장 
            user=user,  # 각 필드에서 입력한 값들
            store_name=self.cleaned_data.get('store_name'), 
            store_img=self.cleaned_data.get('store_img'),
            store_num=self.cleaned_data.get('store_num'), 
            store_address=self.cleaned_data.get('store_address'), 
            store_zipcode=self.cleaned_data.get('store_zipcode'), 
            store_telnum=self.cleaned_data.get('store_telnum'))
        
        return user # 최종적으로 생성된 판매자 객체를 반환
    
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(),label='아이디')
    password = forms.CharField(widget=forms.PasswordInput(),label='비밀번호')



class CustomerEditForm(forms.ModelForm):  # 구매자 계정 회원정보수정 폼
    class Meta:
        model = Customer
        fields = ['cus_nickname', 'cus_name', 'cus_img', 'cus_height', 'cus_weight', 'cus_job', 'cus_address', 'cus_zipcode', 'cus_birth', 'cus_telnum']


class StoreEditForm(forms.ModelForm):  # 판매자 계정 회원정보수정 폼
    class Meta:
        model = Store
        fields = ['store_name', 'store_img', 'store_num', 'store_address', 'store_zipcode', 'store_telnum']
