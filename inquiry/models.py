from django.db import models
from users.models import Customer, Store  # 사용자 및 상점 모델 임포트
from logistics.models import Product  # 상품 모델 임포트

class Question(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # 상품 문의를 한 사용자

    question = models.AutoField(primary_key=True)  
    product = models.ForeignKey('logistics.Product', on_delete=models.CASCADE)

    question_title = models.CharField(max_length=30)
    question_content = models.TextField()
    question_date = models.DateField()

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.AutoField(primary_key=True)
    
    answer_content = models.TextField()
    answer_date = models.DateTimeField(null=True)

    class Meta:
        # 하나의 질문에 대해 여러 개의 답변을 허용하지 않음
        unique_together = ('question',)
