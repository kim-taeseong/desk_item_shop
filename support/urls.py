from django.urls import path
from . import views

urlpatterns = [
    path('store/questions/', views.question_list, name='store_question'),
    path('customer/questions/', views.my_questions, name='customer_question'),
]