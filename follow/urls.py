from django.urls import path
from . import views

urlpatterns = [
    path('', views.follow_and_unfollow, name='follow_and_unfollow'),
]