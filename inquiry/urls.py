from django.urls import path
from .views import create_answer, create_question, question_list, my_questions

app_name='inquiry'

urlpatterns = [
    path('qna/list/', question_list, name='QnA_list'),
    
    path('question/', create_question, name='question_create'),
    path('answer/<int:question_id>/', create_answer, name='answer_create'),

    path('myqna/', my_questions, name='my_qna'),

]