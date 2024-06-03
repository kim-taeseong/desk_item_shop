from django.urls import path
from . import views

urlpatterns = [
    path('store/questions/add/', views.question_list, name='store_question'),
    path('customer/questions/add/', views.my_questions, name='customer_question'),
]