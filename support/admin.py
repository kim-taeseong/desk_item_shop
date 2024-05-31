from django.contrib import admin
from .models import Customer_Question, Store_Question, Answer

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1

class CustomerQuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('customer', 'question_title', 'question_date')

class StoreQuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('store', 'question_title', 'question_date')

admin.site.register(Customer_Question, CustomerQuestionAdmin)
admin.site.register(Store_Question, StoreQuestionAdmin)
