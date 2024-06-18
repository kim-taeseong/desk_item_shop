from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from users.decorators import customer_required, store_required
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.views.generic import *
from .models import Product

#--- store
# 스토어 질문 확인
@login_required(login_url='users:login')
@store_required
def storeQ_list(request):
    store_products = Product.objects.filter(store=request.user.store)
    questions = Question.objects.filter(product__in=store_products)
    template_name = 'store_list.html'
    context = {
        'object_list': questions
    }
    return render(request, template_name, context)

# 상품 답변하기
@login_required(login_url='users:login')
@store_required
def create_answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.save()
            return redirect('inquiry:store_list')
    else:
        form = AnswerForm()
    return render(request, 'answer.html', {'form': form, 'question': question})

# -----------------------------------------

#-- customer
# 질문 작성하기
@login_required(login_url='users:login')
@customer_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.customer = request.user.customer
            question.save()
            # 등록 후에 'QnA_list' 페이지로 리디렉션
            return redirect('inquiry:customer_list')
    else:
        form = QuestionForm()

    return render(request, 'question.html', {'form': form})

# 내 질문목록
@login_required(login_url='users:login')
@customer_required
def customer_questions(request):
    # 현재 로그인한 유저가 작성한 상품문의 내역을 가져옵니다.
    questions = Question.objects.filter(customer=request.user.customer)

    if not questions:
        return render(request, 'none_question.html')

    return render(request, 'cus_list.html', {'user_questions': questions})