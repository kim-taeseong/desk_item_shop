from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import StoreQuestionForm, CustomerQuestionForm
from .models import Store_Question, Customer_Question
from users.decorators import customer_required, store_required


# customer 
# main페이지
def customer_main(request):
    return render(request, 'customer/main.html')

# 질문 하기
@login_required(login_url='users:login')
@customer_required
def customer_question(request):
    if request.method == 'POST':
        form = CustomerQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.customer = request.user.customer
            question.save()
            return redirect('support:QnA_list')
    else:
        form = CustomerQuestionForm()
    
    questions = Customer_Question.objects.filter(customer=request.user.customer)
    return render(request, 'customer/add.html', {'questions': questions, 'form': form})

# 질문 목록
@login_required(login_url='users:login')
@customer_required
def customer_list(request, question_id=None):
    if question_id:
        # 단일 질문의 상세 정보를 가져와야 할 경우
        question = Customer_Question.objects.get(id=question_id)
        return render(request, 'customer/detail.html', {'question': question})
    else:
        # 모든 질문 목록을 가져와야 할 경우
        customer_questions = Customer_Question.objects.filter(customer=request.user.customer).prefetch_related('answers')
        return render(request, 'customer/list.html', {'questions': customer_questions})

# 질문 상세 정보
@login_required(login_url='users:login')
@customer_required
def customer_detail(request, question_id):
    question = get_object_or_404(Customer_Question, id=question_id)
    return render(request, 'customer/detail.html', {'question': question})

# -----------------------------------------

# store
# main페이지
def support_home(request):
    return render(request, 'customer/main.html')

# 질문 하기
@login_required(login_url='users:login')
@customer_required
def customer_question(request):
    if request.method == 'POST':
        form = CustomerQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.customer = request.user.customer
            question.save()
            return redirect('support:QnA_list')
    else:
        form = CustomerQuestionForm()
    
    questions = Customer_Question.objects.filter(customer=request.user.customer)
    return render(request, 'customer/add.html', {'questions': questions, 'form': form})

# 질문 목록
@login_required(login_url='users:login')
@customer_required
def customer_list(request, question_id=None):
    if question_id:
        # 단일 질문의 상세 정보를 가져와야 할 경우
        question = Customer_Question.objects.get(id=question_id)
        return render(request, 'customer/detail.html', {'question': question})
    else:
        # 모든 질문 목록을 가져와야 할 경우
        customer_questions = Customer_Question.objects.filter(customer=request.user.customer).prefetch_related('answers')
        return render(request, 'customer/list.html', {'questions': customer_questions})


