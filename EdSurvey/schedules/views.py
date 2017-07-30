# from django.db.models.query_utils import Q
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.timezone import now

from .models import Schedule, Attempt   # , Task
# from surveys.views import render_run_attempt


def render_run_attempt(schedule):
    """ Генерирует HTML-код для отображения возможности запуска попытки пройти тест"""
    # проверить, что мы в сроках
    if schedule.start < now() < schedule.finish:
        # найти незавершённую попытку
        attempt = Attempt.objects.all().filter(schedule=schedule,
                                               finished__isnull=True)   # .oreder_by('-started')
        if attempt:
            # и вернуть HTML-код запуска теста
            return render_to_string('runattemptblock.html', {'attempt': attempt[0]})
        # Если незавершённой попытки нет, то Вычислить количество доступных попыток
        elif schedule.task.attempts > Attempt.objects.all().filter(schedule=schedule,
                                                                   finished__isnull=False).count():
            # Если есть досупные попытки, то вернуть HTML-код запуска теста
            return render_to_string('newattemptblock.html', {'schedule': schedule})
        else:
            # Если все попытки использованы, то сообщить об остутсвие доступных попыток из _имеющихся_
            return render_to_string('noattemptblock.html', {'attempts': schedule.attempts})
    else:
        return render_to_string('outofdateblock.html', {'attempts': schedule.attempts})


def schedule_info(request, scheduleid):
    schedule = get_object_or_404(Schedule, pk=scheduleid)
    return render(request,
                  'scheduleinfo.html',
                  {
                      'infoblock': render_schedule_info(schedule),
                      'taskinfoblock': render_task_info(schedule.task),
                      'runattemptblock': render_run_attempt(schedule),
                  },
                  )


def render_schedule_info(schedule):
    """ Генерация HTML-блока с описанием параметров расписания"""
    return render_to_string('scheduleinfoblock.html', {'schedule': schedule})


def render_task_info(task):
    """ Генерация HTML-блока с описанием параметров задания"""
    return render_to_string('taskinfoblock.html', {'task': task})


# def task_info(request, taskid):
#     task = get_object_or_404(Task, pk=taskid)
#     return render(request, 'taskinfo.html', {'task': task})


def run_attempt(request, attemptid):
    """ Показать общую информацию о параметрах
    - задания
    - тест-кейса
    - конкретной попытки
    """
    attempt = get_object_or_404(Attempt, pk=attemptid)
    return render(
        request,
        'runattempt.html',
        {
            'attempt': attempt,
            'taskinfoblock': render_task_info(attempt.schedule.task),
            # 'querylistinfoblock': render_querylist_info(attempt.schedule.task.querylist),
        },
    )


def new_attempt(request, scheduleid):
    attempt = Attempt(schedule=get_object_or_404(Schedule, pk=scheduleid))
    attempt.save()
    return run_attempt(request, attempt.id)


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
