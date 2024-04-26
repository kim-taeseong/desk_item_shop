from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.customer_home, name="customer-home"),
    path("store/", views.store_home, name="store-home"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("signup/customer/", views.CustomerSignUpView.as_view(), name="customer-signup"),
    path("signup/store/", views.StoreSignUpView.as_view(), name="store-signup"),
    path('logout/', auth_views.LogoutView.as_view(template_name="users/logout.html"), name="logout"),
]