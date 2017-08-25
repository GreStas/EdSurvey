from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404

from clients.models import Person, RolePermission
from .models import Question, RADIOBUTTON, CHECKBOX, LINKEDLISTS, Answer, AnswerRB, AnswerCB, AnswerLL


def index(request):
    person = Person.objects.get(pk=request.session['person_id'])
    qowner = Question.objects.all().filter(owner=person)
    qpublic = Question.objects.all().filter(public=True)
    try:
        perms = RolePermission.objects.all().get(role=person.role, datatype__applabel='questions', datatype__model='Question')
        print(perms.acl)
        if 'L' in perms.acl:
            qdivision = Question.objects.all().filter(division=person.division)
            questions = qowner.union(qpublic).union(qdivision)
        else:
            questions = qowner.union(qpublic)
    except ObjectDoesNotExist:
        questions = qowner.union(qpublic)
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
