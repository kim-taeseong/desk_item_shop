from django import forms
from .models import Customer_Question, Store_Question

class CustomerQuestionForm(forms.ModelForm):
    class Meta:
        model = Customer_Question
        fields = ['question_title', 'question_content']

class StoreQuestionForm(forms.ModelForm):
    class Meta:
        model = Store_Question
        fields = ['question_title', 'question_content']
