from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from users.decorators import customer_required, store_required
from django.urls import reverse
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.views.generic import *
from .models import Product

@login_required(login_url='users:login')
@store_required
def question_list(request):
    store_products = Product.objects.filter(store=request.user.store)
    questions = Question.objects.filter(product__in=store_products)
    template_name = 'QnA_list.html'
    context = {
        'object_list': questions
    }
    return render(request, template_name, context)

@login_required(login_url='users:login')
@customer_required
def my_questions(request):
    # 현재 로그인한 유저가 작성한 상품문의 내역을 가져옵니다.
    user_questions = Question.objects.filter(customer=request.user.customer)

    if not user_questions:
        return render(request, 'none_question.html')

    return render(request, 'user_QnA.html', {'user_questions': user_questions})


@login_required(login_url='users:login')
@customer_required
def create_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.customer = request.user.customer
            question.save()
            # 등록 후에 'my_qna' 페이지로 리디렉션, 질문의 ID를 전달
            return redirect('inquiry:my_qna')  # 질문의 ID를 전달
    else:
        form = QuestionForm()

    return render(request, 'question.html', {'form': form})





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
            return redirect('inquiry:QnA_list')
    else:
        form = AnswerForm()
    return render(request, 'answer.html', {'form': form, 'question': question})
    
