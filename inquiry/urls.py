from django.urls import path
from .views import create_answer, create_question, storeQ_list, customer_questions

app_name='inquiry'

urlpatterns = [
    
    #store
    path('qna/list/', storeQ_list, name='store_list'), #store Q&A 목록
    path('answer/<int:question_id>/', create_answer, name='answer_create'), # 답변 등록
    
    #customer
    path('question/', create_question, name='question_create'), # 질문 등록
    path('question/not/', customer_questions, name='none_question'), # 작성된 질문 없을 때
    path('myqna/', customer_questions, name='customer_list'), # 내가 질문한 목록

]