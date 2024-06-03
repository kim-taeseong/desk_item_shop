from django.urls import path
from . import views

app_name = 'support'
urlpatterns = [    
    #질문한 내역
    path('cus/list/', views.QnA_list, name='QnA_list'),
    path('store/list/', views.QnA_list, name='QnA_list'),

    # 질문 내용 및 답변 상세페이지
    path('cus/<int:question_id>/', views.QnA_list, name='QnA_detail'),
    path('store/<int:question_id>/', views.QnA_list, name='QnA_detail'),

    #질문 하기
    path('store/questions/add/', views.store_question, name='store_question'),
    path('customer/questions/add/', views.customer_question, name='customer_question'),
]