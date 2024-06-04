from django.db import models
from users.models import Customer, Store

class Customer_Question(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='questions', verbose_name="고객")
    question_title = models.CharField(max_length=30, verbose_name="제목")
    question_content = models.TextField(verbose_name="내용")
    question_date = models.DateTimeField(auto_now_add=True, verbose_name="등록일")

    def __str__(self):
        return f"{self.customer.cus_name}님의 질문: {self.question_title[:50]}"

class Store_Question(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='questions', verbose_name="상점")
    question_title = models.CharField(max_length=30, verbose_name="제목")
    question_content = models.TextField(verbose_name="내용")
    question_date = models.DateTimeField(auto_now_add=True, verbose_name="등록일")

    def __str__(self):
        return f"{self.store.store_name}님에게 된 질문: {self.question_title[:50]}"

class Answer(models.Model):
    customer_question = models.ForeignKey(Customer_Question, on_delete=models.CASCADE, null=True, blank=True, related_name='answers', verbose_name="질문")
    store_question = models.ForeignKey(Store_Question, on_delete=models.CASCADE, null=True, blank=True, related_name='answers', verbose_name="질문")
    answer_content = models.TextField(verbose_name="내용")
    answer_date = models.DateTimeField(auto_now_add=True, verbose_name="등록일")

    def __str__(self):
        return f"답변: {self.answer_content[:50]}"
