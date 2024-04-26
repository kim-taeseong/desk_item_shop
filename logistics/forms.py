from django import forms
from .models import Category

class ProductSearchForm(forms.Form):
    # 카테고리 선택 필드
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label='전체 카테고리', required=False)
    # 상품명 입력 필드
    product_name = forms.CharField(label='상품명', max_length=100, required=False)
