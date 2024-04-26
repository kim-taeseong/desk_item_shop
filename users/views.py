from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .models import User, Customer, Store
from logistics.models import Product
from .forms import CustomerSignUpForm, StoreSignUpForm, LoginForm
from django.contrib.auth import login
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .decorators import customer_required, store_required

class CustomerSignUpView(CreateView):
    model = User
    form_class = CustomerSignUpForm
    template_name = 'users/customer_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'customer'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('customer-home')
    
class StoreSignUpView(CreateView):
    model = User
    form_class = StoreSignUpForm
    template_name = 'users/store_signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'store'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('store-home')
    
class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_customer:
                return reverse('customer-home')
            elif user.is_store:
                return reverse('store-home')
        else:
            return reverse('login')
        
@login_required
@customer_required
def customer_home(request):
    product = Product.objects.all()
    context = {
        'products': product
    }
    return render(request, 'users/customer_home.html', context)

@login_required
@store_required
def store_home(request):
    product = Product.objects.all()
    context = {
        'products': product
    }
    return render(request, 'users/store_home.html', context)