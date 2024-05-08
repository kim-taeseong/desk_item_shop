from django import forms
from django.utils import timezone  # 시간대를 다루는 데 사용되는 모듈
from .models import Question, Answer

class QuestionForm(forms.ModelForm):
    question_date = forms.DateField(initial=timezone.now)  # 오늘 날짜로 초기화
    
    class Meta:
        model = Question
        fields = ['product', 'question_title', 'question_content', 'question_date']

class AnswerForm(forms.ModelForm):
    answer_date = forms.DateField(initial=timezone.now)  # 오늘 날짜로 초기화
    
    class Meta:
        model = Answer
        fields = ['answer_content', 'answer_date']
