from django.urls import path
from . import views

urlpatterns = [
    path('save_and_remove_store/', views.save_and_remove_store, name='save_and_remove_store'),
]
