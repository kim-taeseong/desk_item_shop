from django.contrib import admin
from .models import Question, Answer

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_title', 'customer', 'product', 'question_date')
    search_fields = ('question_title', 'customer__username', 'product__name')
    list_filter = ('question_date',)
    ordering = ('-question_date',)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer_date')
    search_fields = ('question__question_title',)
    list_filter = ('answer_date',)
    ordering = ('-answer_date',)

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
