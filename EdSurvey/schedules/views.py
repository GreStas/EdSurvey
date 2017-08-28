# schedules.views
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.utils.timezone import now

from .models import Schedule, Task
from clients.models import Person


@login_required(login_url='login')
def attempt_auth_or_404(request, attempt):
    if attempt.user != request.user:
        raise ObjectDoesNotExist


@login_required(login_url='login')
def schedule_index(request):
    person = Person.objects.get(pk=request.session['person_id'])
    opened_schedules = Schedule.objects.perm(person=person, acl='L').filter(start__lt=now(), finish__gt=now()).order_by('task__id', '-start', 'name')
    closed_schedules = Schedule.objects.perm(person=person, acl='L').filter(finish__lt=now()).order_by('task__id', '-start', '-finish', 'name')
    return render(
        request,
        'schedules.html',
        {
            'opened': opened_schedules,
            'closed': closed_schedules,
        }
    )


@login_required(login_url='login')
def task_index(request):
    person = Person.objects.get(pk=request.session['person_id'])
    tasks = Task.objects.perm(person=person, acl='L').order_by('id')
    return render(
        request,
        'tasks.html',
        {
            'tasks': tasks,
        }
    )


@login_required(login_url='login')
def index(request):
    """!!! Полный вид без учёта прав - убрать на ПРОДе !!!"""
    tasks = Task.objects.all().order_by('id')
    opened_schedules = Schedule.objects.all().filter(start__lt=now(), finish__gt=now()).order_by('task', '-start', 'name')
    closed_schedules = Schedule.objects.all().filter(finish__lt=now()).order_by('task', '-start', '-finish', 'name')
    return render(
        request,
        'schedulesapp.html',
        {
            'tasks': tasks,
            'opened': opened_schedules,
            'closed': closed_schedules,
        }
    )
