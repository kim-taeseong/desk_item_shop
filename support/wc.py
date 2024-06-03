from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.decorators import store_required, customer_required
from .models import Customer_Question, Store_Question
from .forms import CustomerQuestionForm, StoreQuestionForm

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


# 로그인이 필요하고, 고객인 경우에만 접근 가능한 뷰
@login_required(login_url='users:login')
@customer_required
def customer_question(request):
    if request.method == 'POST':  # POST 요청인 경우
        form = CustomerQuestionForm(request.POST)  # 폼 데이터로부터 폼 생성
        if form.is_valid():  # 폼이 유효한지 확인
            question = form.save(commit=False)  # 폼 데이터를 기반으로 질문 객체 생성
            question.customer = request.user.customer  # 현재 로그인한 사용자와 연결된 고객 설정
            question.save()  # 데이터베이스에 질문 객체 저장
            return redirect('support:customer_question')  # 질문 제출 후 해당 페이지로 리디렉션
    else:  # POST 요청이 아닌 경우
        form = CustomerQuestionForm()  # 빈 폼 생성
    
    # 현재 사용자와 관련된 모든 질문 가져오기
    questions = Customer_Question.objects.filter(customer=request.user.customer)
    
    # 질문 제출 폼과 이전에 제출한 질문 목록을 페이지에 표시
    return render(request, 'cus_Q.html', {'questions': questions, 'form': form})


@login_required(login_url='users:login')
@customer_required
def customer_list(request):
    customer_questions = Customer_Question.objects.filter(customer=request.user.customer).prefetch_related('answers')
    template_name = 'QnA_list.html'
    context = {
        'questions': customer_questions
    }
    return render(request, template_name, context)


@login_required(login_url='users:login')
@store_required
def store_list(request):
    store_questions = Store_Question.objects.filter(store=request.user.store).prefetch_related('answers')
    template_name = 'QnA_list.html'
    context = {
        'questions': store_questions
    }
    return render(request, template_name, context)


# 현재 로그인한 유저가 작성한 상품문의 내역을 가져옵니다.
@login_required(login_url='users:login')
@customer_required
def QnA_list(request):
    customer_questions = Customer_Question.objects.filter(customer=request.user.customer).prefetch_related('answers')
    template_name = 'QnA.html'
    context = {
        'questions': customer_questions
    }
    return render(request, template_name, context)