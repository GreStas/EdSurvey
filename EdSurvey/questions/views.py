from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from clients.models import Person, RolePermission
from .models import Question, RADIOBUTTON, CHECKBOX, LINKEDLISTS, Answer, AnswerRB, AnswerCB, AnswerLL


@login_required(login_url='login')
def index(request):
    person = Person.objects.get(pk=request.session['person_id'])
    questions = Question.objects.perm(person=person, acl='L')
    return render(
        request,
        'questions.html',
        {'questions': questions},
    )


def answers_by_question(request, questionid):
    question = get_object_or_404(Question, pk=questionid)
    if question.qtype in [RADIOBUTTON, CHECKBOX]:
        answers = Answer.objects.filter(question=question)
        return render(
            request,
            'answersbyquestion.html',
            {'question': question,
             'answers': answers}
        )
    elif question.qtype in [LINKEDLISTS]:
        answers = AnswerLL.objects.filter(question=question)
        return render(
            request,
            'answersllbyquestion.html',
            {'question': question,
             'answers': answers}
        )
