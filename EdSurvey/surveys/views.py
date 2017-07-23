from django.shortcuts import render, get_object_or_404
from schedules.models import Schedule, Task
from .models import Attempt


def index(request):
    """ Показать количество
    - Назначенных аданий        [подробнее >] переход на view выбора задания choice_run с соответсвующим фильтром
        - Не начатых заданий    [подробнее >] переход на view выбора задания choice_run с соответсвующим фильтром
        - Незавершённых заданий [подробнее >] переход на view выбора задания choice_run с соответсвующим фильтром
    - Пройденных заданий        [подробнее >] переход на view выбора пройденного задания choice_done
    """
    cnt_avalaible = Schedule.objects.all().count()  # .filter(now between start and finish and не все попытки использованы)
    cnt_notstarted = Schedule.objects.all().count()  # .filter(now between start and finish and не все попытки использованы and shcedule not in attempts)
    cnt_notfinished = Schedule.objects.all().count()  # .filter(now between start and finish and не все попытки использованы and shcedule in attempts)
    cnt_done = Schedule.objects.all().count()  # .filter(now >= finish or now between start and finish and все попытки использованы)
    return render(
        request,
        'surveyscommon.html',
        {
            'cnt_avalaible': cnt_avalaible,
            'cnt_notstarted': cnt_notstarted,
            'cnt_notfinished': cnt_notfinished,
            'cnt_done': cnt_done,
        },
    )


def choice_run(request):
    schedules = Schedule.objects.all()
    return render(
        request,
        'choicerun.html',
        {'schedules': schedules},
    )


def choice_done(request):
    schedules = Schedule.objects.all()
    return render(
        request,
        'choicedone.html',
        {'schedules': schedules},
    )


def choice_attempt(request, scheduleid):
    """ Выбор варианта дальнейших действий в зависимости от наличия доступных попыток.
    1. Если есть незавершённая попытка, то предложить продолжить выполнение.
    2. Если нет незавершённых попыток и есть ещё неиспользованные поптки, то предложить начать выполнение.
    3. Если попыток нет, то вывести сообщение "Обратитесь к менеджеру."
    """
    CONTINUE_ATTEMPT = 1
    NEW_ATTEMPT = 2
    NO_ATTEMPT = 3

    schedule = get_object_or_404(Schedule, pk=scheduleid)
    var = NO_ATTEMPT  # TODO Заменить на код по определению выбору варианта дальнейших действий

    if var == CONTINUE_ATTEMPT:    # Продолжить выполнение - continueattempt
        # Форма выбора
        # [Продолжить] - вызовет run_attempt(schedule, attempt)
        # [Отмена] - вызовет index()
        attempts = Attempt.objects.all().filter(schedule=schedule)
        return render(
            request,
            'continueattempt.html',
            {
                'schedule': schedule,
                'attempts': attempts,
            },
        )
    elif var == NEW_ATTEMPT:  # Новая попытка - newattempt
        # Форма выбора
        # [Начать] - Создаст новую попытку и вызовет run_attempt(schedule, attempt)
        # [Отмена] - вызовет index()
        attempts = Attempt.objects.all().filter(schedule=schedule)  # проверку на достаточность попыток сделает валидатор или *save() в Attempt
        return render(
            request,
            'newattempt.html',
            {
                'schedule': schedule,
                'attempts': attempts,
            },
        )
    elif var == NO_ATTEMPT:
        # Покажет параметры расписания, совершённые попытки и соответствующее сообщение
        attempts = Attempt.objects.all().filter(schedule=schedule).order_by('-started')
        return render(
            request,
            'noattempt.html',
            {
                'schedule': schedule,
                'attempts': attempts,
            },
        )
    # TODO return Что-нибудь про внутреннюю ошибку.


def run_attempt(request, attemptid):
    return render(
        request,
        'run_attempt.html',
        {'attemptid': attemptid},
    )
