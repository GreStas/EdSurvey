from django.shortcuts import render, get_object_or_404
from .models import Question, Answer, AnswerRB, AnswerCB, AnswerLL


def index(request):
    questions = Question.objects.all()
    return render(
        request,
        'questions.html',
        {'questions': questions},
    )

def answers_by_question(request, questionid):
    question = get_object_or_404(Question, pk=questionid)
    if question.qtype in [Question.RADIOBUTTON, Question.CHECKBOX]:
        answers = Answer.objects.filter(question=question)
        return render(
            request,
            'answersbyquestion.html',
            {'question': question,
             'answers': answers}
        )
    elif question.qtype in [Question.LINKEDLISTS]:
        answers = AnswerLL.objects.filter(question=question)
        return render(
            request,
            'answersllbyquestion.html',
            {'question': question,
             'answers': answers}
        )
