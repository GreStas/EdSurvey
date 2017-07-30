from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.utils.timezone import now
from django.db import transaction

from random import shuffle

from .models import Result, ResultRB, ResultCB, ResultLL
from schedules.models import Schedule, Task, Attempt
from querylists.models import QueryContent
from questions.models import RADIOBUTTON, CHECKBOX, LINKEDLISTS


def generate_result_list(attempt):
    """ Генерирует последовательность Result
    1. Выбрать упорядоченные
select * from querylists_querycontent where ordernum is not null and querylist_id in
(select id from querylists_querylist where id in
	(select querylist_id from schedules_task where id in
		(select task_id from schedules_schedule where id in
			(select schedule_id from schedules_attempt where id = 3)
		)
	)
)
order by ordernum

    2. Выбрать неупорядоченные
select * from querylists_querycontent where ordernum is null and querylist_id in
(select id from querylists_querylist where id in
	(select querylist_id from schedules_task where id in
		(select task_id from schedules_schedule where id in
			(select schedule_id from schedules_attempt where id = 3)
		)
	)
)

    3. Перемешать неупорядоченный список.

    4. Соединить два списка - сначала упорядоченные.

    5. BEGIN TRANSACTION ( Создать последовательность Result по [].question.id ) END TRANSACTION
    """
    task = Task.objects.get(schedule__attempt=attempt)
    ordered_contents = QueryContent.objects.all().filter(querylist=task.querylist, ordernum__isnull=False)
    unordered_contents = QueryContent.objects.all().filter(querylist=task.querylist, ordernum__isnull=True)
    shuffle(unordered_contents)
    contents = ordered_contents.union(unordered_contents)

    with transaction.atomic():
        for i,content in enumerate(contents):
            r = Result(
                attempt=attempt,
                question=content.question,
                ordernum=i,
            )
            r.save()


def prev_result(attempt, curr_result):
    """ Перемещается назад по Anketa """
    result = None
    return result


def next_result(attempt, curr_result):
    """ Перемещается вперёд по Anketa """
    result = None
    return result


def run_attempt(request, attemptid):
    attempt = get_object_or_404(Attempt, pk=attemptid)
    generate_result_list(attempt)
    result = get_object_or_404(Result, attempt=attempt, ordernum=0)
    if result.question.qtype == RADIOBUTTON:
        return redirect(
            request,
            'radiobutton.html',
            {
                'result': result,
            }
        )
    elif result.question.qtype == CHECKBOX:
        pass
    elif result.question.qtype == LINKEDLISTS:
        pass
    # else:
    #     return internal_error


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
