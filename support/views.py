from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import StoreQuestionForm, CustomerQuestionForm
from .models import Store_Question, Customer_Question
from users.decorators import customer_required, store_required

def support_home(request):
    return render(request, 'support_home.html')

@login_required(login_url='users:login')
@store_required
def store_question(request):
    if request.method == 'POST':
        form = StoreQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.store = request.user.store
            question.save()
            return redirect('support:store_question')
    else:
        form = StoreQuestionForm()
    
    questions = Store_Question.objects.filter(store=request.user.store)
    return render(request, 'store_Q.html', {'questions': questions, 'form': form})

@login_required(login_url='users:login')
@customer_required
def customer_question(request):
    if request.method == 'POST':
        form = CustomerQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.customer = request.user.customer
            question.save()
            return redirect('support:customer_question')
    else:
        form = CustomerQuestionForm()
    
    questions = Customer_Question.objects.filter(customer=request.user.customer)
    return render(request, 'cus_Q.html', {'questions': questions, 'form': form})

@login_required(login_url='users:login')
@customer_required
def QnA_list(request, question_id=None):
    if question_id:
        # 단일 질문의 상세 정보를 가져와야 할 경우
        question = Customer_Question.objects.get(id=question_id)
        return render(request, 'QnA_detail.html', {'question': question})
    else:
        # 모든 질문 목록을 가져와야 할 경우
        customer_questions = Customer_Question.objects.filter(customer=request.user.customer).prefetch_related('answers')
        return render(request, 'QnA.html', {'questions': customer_questions})
