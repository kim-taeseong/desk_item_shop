from django.urls import path
from . import views

urlpatterns = [
    path('profile/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('profile/<int:user_id>/follow/', views.follow, name='follow'),
    path('profile/<int:user_id>/unfollow/', views.unfollow, name='unfollow'),
]
