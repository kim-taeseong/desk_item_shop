from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.decorators import store_required, customer_required
from .models import Customer_Question, Store_Question
from .forms import CustomerQuestionForm, StoreQuestionForm

# @login_required(login_url='users:login')
# @store_required
def question_list(request):
    if request.method == 'POST':
        form = StoreQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.store = request.user.store
            question.save()
            return redirect('question_list')
    else:
        form = StoreQuestionForm()
    
    questions = Store_Question.objects.filter(store=request.user.store)
    return render(request, 'support/store_question_list.html', {'questions': questions, 'form': form})

# @login_required(login_url='users:login')
# @customer_required
def my_questions(request):
    if request.method == 'POST':
        form = CustomerQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.customer = request.user.customer
            question.save()
            return redirect('my_questions')
    else:
        form = CustomerQuestionForm()
    
    questions = Customer_Question.objects.filter(customer=request.user.customer)
    return render(request, 'support/customer_question_list.html', {'questions': questions, 'form': form})
