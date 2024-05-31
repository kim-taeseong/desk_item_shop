from django.urls import path
from . import views

urlpatterns = [
    path('store/questions/', views.question_list, name='question_list'),
    path('customer/questions/', views.my_questions, name='my_questions'),
]