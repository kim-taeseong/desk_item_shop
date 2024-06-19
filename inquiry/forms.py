from django import forms
from django.utils import timezone  # 시간대를 다루는 데 사용되는 모듈
from .models import Question, Answer
from logistics.models import Product  # 상품 모델 임포트

class QuestionForm(forms.ModelForm):
    # 상품 선택 드롭다운 목록 추가
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label=None)

    class Meta:
        model = Question
        fields = ['product', 'question_title', 'question_content']

class AnswerForm(forms.ModelForm):
    answer_date = forms.DateField(initial=timezone.now)  # 오늘 날짜로 초기화
    
    class Meta:
        model = Answer
        fields = ['answer_content', 'answer_date']
