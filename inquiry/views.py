from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import customer_required, store_required
from django.urls import reverse
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm
from django.views.generic import *

@login_required
@store_required
def question_list(request):
    questions = Question.objects.all()
    template_name = 'QnA_list.html'
    context = {
        'object_list': questions
    }
    return render(request, template_name, context)


def my_questions(request):
    # 현재 로그인한 유저가 작성한 상품문의 내역을 가져옵니다.
    user_questions = Question.objects.filter(customer=request.user.customer)
    return render(request, 'user_QnA.html', {'user_questions': user_questions})


@login_required
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





@login_required
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
    
