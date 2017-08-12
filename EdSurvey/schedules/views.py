# schedules.views
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.utils.timezone import now

from .models import Schedule, Attempt
from querylists.views import render_querylist_info


@login_required(login_url='login')
def attempt_auth_or_404(request, attempt):
    if attempt.user != request.user:
        raise ObjectDoesNotExist


@login_required(login_url='login')
def render_run_attempt(request, schedule):
    """ Генерирует HTML-код для отображения возможности запуска попытки пройти тест"""
    # проверить, что мы в сроках
    if schedule.start < now() < schedule.finish:
        # найти незавершённую попытку
        attempt = Attempt.objects.all().filter(schedule=schedule,
                                               finished__isnull=True,
                                               user=request.user).order_by('-started')
        if len(attempt):
            # и вернуть HTML-код запуска теста
            return render_to_string('runattemptblock.html', {'attempt': attempt[0]})
        # Если незавершённой попытки нет, то Вычислить количество доступных попыток
        elif schedule.task.attempts > Attempt.objects.all().filter(schedule=schedule,
                                                                   finished__isnull=False,
                                                                   user=request.user).count():
            # Если есть досупные попытки, то вернуть HTML-код запуска теста
            return render_to_string('newattemptblock.html', {'schedule': schedule})
        else:
            # Если все попытки использованы, то сообщить об остутсвие доступных попыток из _имеющихся_
            return render_to_string('noattemptblock.html', {'attempts': schedule.task.attempts})
    else:
        return render_to_string('outofdateblock.html', {'attempts': schedule.task.attempts})


@login_required(login_url='login')
def render_attempt_list(request, schedule):
    attempts = Attempt.objects.all().filter(schedule=schedule, user=request.user).order_by('-started')
    return render_to_string('attemptlistblock.html', {'attempts': attempts})


@login_required(login_url='login')
def render_schedule_info(request, schedule):
    """ Генерация HTML-блока с описанием параметров расписания"""
    return render_to_string('scheduleinfoblock.html', {'schedule': schedule})


@login_required(login_url='login')
def schedule_info(request, scheduleid):
    schedule = get_object_or_404(Schedule, pk=scheduleid)
    return render(request,
                  'scheduleinfo.html',
                  {
                      'scheduleinfoblock': render_schedule_info(request, schedule),
                      'taskinfoblock': render_task_info(request, schedule.task),
                      'runattemptblock': render_run_attempt(request, schedule),
                      'querylistinfoblock': render_querylist_info(request, schedule.task.querylist),
                      'attemptlistblock': render_attempt_list(request, schedule)
                  },
                  )


@login_required(login_url='login')
def render_task_info(request, task):
    """ Генерация HTML-блока с описанием параметров задания"""
    return render_to_string('taskinfoblock.html', {'task': task})


@login_required(login_url='login')
def run_attempt(request, attemptid):
    return redirect(reverse('surveys:runattempt', args=[attemptid]))


@login_required(login_url='login')
def new_attempt(request, scheduleid):
    schedule = get_object_or_404(Schedule, pk=scheduleid)
    # Проверим использование доступных попыток
    attempts = Attempt.objects.all().filter(schedule=schedule, finished__isnull=False, user=request.user).count()
    if attempts >= schedule.task.attempts:
        raise ValidationError("Использованы все доступные попытки.")
    try:
        # Если есть незавершённая попытка, то используем её
        attempt = Attempt.objects.get(schedule=schedule, finished__isnull=True, user=request.user)
    except ObjectDoesNotExist:
        # Если нет незавершённой попытки, то создаём новую
        attempt = Attempt(schedule=schedule, user=request.user)
        attempt.save()
    return run_attempt(request, attempt.id)


@login_required(login_url='login')
def index(request):
    opened_schedules = Schedule.objects.all().filter(start__lt=now(), finish__gt=now())
    closed_schedules = Schedule.objects.all().filter(finish__lt=now())
    return render(
        request,
        'schedules.html',
        {
            'opened': opened_schedules,
            'closed': closed_schedules,
        }
    )
