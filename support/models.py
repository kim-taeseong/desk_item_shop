from django.db import models
from users.models import Customer, Store

class Customer_Question(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='questions')
    question_title = models.CharField(max_length=30)
    question_content = models.TextField()
    question_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question from {self.customer.cus_name}: {self.question_title[:50]}"

class Store_Question(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='questions')
    question_title = models.CharField(max_length=30)
    question_content = models.TextField()
    question_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Question for {self.store.store_name}: {self.question_title[:50]}"

class Answer(models.Model):
    customer_question = models.ForeignKey(Customer_Question, on_delete=models.CASCADE, null=True, blank=True, related_name='answers')
    store_question = models.ForeignKey(Store_Question, on_delete=models.CASCADE, null=True, blank=True, related_name='answers')
    answer_content = models.TextField()
    answer_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer: {self.answer_content[:50]}"
