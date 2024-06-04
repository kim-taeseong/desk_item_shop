from django.urls import path
from . import views

app_name = 'support'
urlpatterns = [

    #customer
    path('', views.customer_main, name='main'),
    path('cus/list/', views.customer_list, name='customer_list'), # 질문한 내역
    path('cus/<int:question_id>/', views.customer_detail, name='customer_detail'), # 상세페이지
    path('customer/questions/add/', views.customer_question, name='customer_question'), # 질문하기


    #store
    path('', views.customer_main, name='support_home'),
    path('store/list/', views.customer_list, name='QnA_list'), # 질문한 내역
    path('store/<int:question_id>/', views.customer_list, name='QnA_detail'), # 상세페이지
    path('store/questions/add/', views.customer_question, name='customer_question'), # 질문하기
]