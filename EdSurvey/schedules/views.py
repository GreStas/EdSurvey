from django.db.models.query_utils import Q
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.timezone import now

from schedules.models import Task, Schedule


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

def task_info(request, taskid):
    task = get_object_or_404(Task, pk=taskid)
    return render(request, 'taskinfo.html', {'task': task})

def schedule_info(request, scheduleid):
    schedule = get_object_or_404(Schedule, pk=scheduleid)
    return render(request,
                  'scheduleinfo.html',
                  {
                      'infoblock': render_schedule_info(schedule),
                      'taskinfoblock': render_task_info(schedule.task)
                  },
                  )

def render_task_info(task):
    """ Генерация HTML-блока с описанием параметров задания"""
    return render_to_string('taskinfoblock.html', {'task': task})

def render_schedule_info(schedule):
    """ Генерация HTML-блока с описанием параметров расписания"""
    return render_to_string('scheduleinfoblock.html', {'schedule': schedule})
