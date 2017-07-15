from django.shortcuts import render, get_object_or_404
from .models import Question, Answer, AnswerLL


def index(request):
    questions = Question.objects.all()
    return render(
        request,
        'index.html',
        {'questions': questions},
    )

def answersbyid(request, questionid):
    question = Question.objects.filter(id=questionid)
    if question[0].qtype in [Question.RADIOBUTTON, Question.CHECKBOX]:
        answers = Answer.objects.filter(question=questionid)
        return render(
            request,
            'answersbyid.html',
            {'question': get_object_or_404(Question, pk=int(questionid)),
             'answers': answers}
        )
    elif question[0].qtype in [Question.LINKEDLISTS]:
        answers = AnswerLL.objects.filter(question=questionid)
        return render(
            request,
            'answersllbyid.html',
            {'question': get_object_or_404(Question, pk=int(questionid)),
             'answers': answers}
        )
