from django.contrib import admin
from .models import Customer_Question, Store_Question, Answer

class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 1
    verbose_name = "답변"
    verbose_name_plural = "답변들"

class CustomerQuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('customer', 'question_title', 'question_date')
    search_fields = ('question_title', 'customer__username')
    list_filter = ('question_date',)
    exclude = ('question_date',)  # 이 필드를 숨깁니다.

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('customer')

    fieldsets = (
        ('기본 정보', {
            'fields': ('customer', 'question_title', 'question_content')
        }),
    )
    ordering = ('-question_date',)

class StoreQuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ('store', 'question_title', 'question_date')
    search_fields = ('question_title', 'store__name')
    list_filter = ('question_date',)
    exclude = ('question_date',)  # 이 필드를 숨깁니다.

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('store')

    fieldsets = (
        ('기본 정보', {
            'fields': ('store', 'question_title', 'question_content')
        }),
    )
    ordering = ('-question_date',)

admin.site.register(Customer_Question, CustomerQuestionAdmin)
admin.site.register(Store_Question, StoreQuestionAdmin)
