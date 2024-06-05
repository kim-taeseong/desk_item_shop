from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import StoreQuestionForm, CustomerQuestionForm
from .models import Store_Question, Customer_Question
from users.decorators import customer_required, store_required


# customer 
# main페이지
@login_required(login_url='users:login')
@customer_required
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
            return redirect('support:customer_list')
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
@login_required(login_url='users:login')
@store_required
def store_main(request):
    return render(request, 'store/main.html')

# 질문 하기
@login_required(login_url='users:login')
@store_required
def store_question(request):
    if request.method == 'POST':
        form = StoreQuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.store = request.user.store
            question.save()
            return redirect('support:store_list')
    else:
        form = StoreQuestionForm()
    
    questions = Store_Question.objects.filter(store=request.user.store)
    return render(request, 'store/add.html', {'questions': questions, 'form': form})

# 질문 목록
@login_required(login_url='users:login')
@store_required
def store_list(request, question_id=None):
    if question_id:
        # 단일 질문의 상세 정보를 가져와야 할 경우
        question = Store_Question.objects.get(id=question_id)
        return render(request, 'store/detail.html', {'question': question})
    else:
        # 모든 질문 목록을 가져와야 할 경우
        store_questions = Store_Question.objects.filter(store=request.user.store).prefetch_related('answers')
        return render(request, 'store/list.html', {'questions': store_questions})

# 질문 상세 정보
@login_required(login_url='users:login')
@store_required
def store_detail(request, question_id):
    question = get_object_or_404(Store_Question, id=question_id)
    return render(request, 'store/detail.html', {'question': question})
