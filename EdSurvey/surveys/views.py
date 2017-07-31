from django.db.models.aggregates import Max
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.utils.timezone import now
from django.db import transaction

from random import shuffle

from .models import Anketa  # , Result, ResultRB, ResultCB, ResultLL
from schedules.models import Schedule, Task, Attempt
from querylists.models import QueryContent
from questions.models import RADIOBUTTON, CHECKBOX, LINKEDLISTS, Question


def generate_anketa(attempt):
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
            a = Anketa(
                attempt=attempt,
                question=content.question,
                ordernum=i,
            )
            a.save()


def run_attempt(request, attemptid):
    attempt = get_object_or_404(Attempt, pk=attemptid)
    # if Anketa.objects.all().filter(attempt=attempt).count() == 0:
    if not len(Anketa.objects.all().filter(attempt=attempt)):
        generate_anketa(attempt)
    query = get_object_or_404(Anketa, attempt=attempt, ordernum=0)
    return redirect(reverse('surveys:showquery', args=[query.id]))


def render_prev_query_button(query):
    return render_to_string(
        '<input type="submit" value="<< Предыдущий" name="prev_query"' + \
        (' disabled' if query.ordernum <= 0 else '') + \
        '>'
    )


def render_next_query_button(query):
    return '<input type="submit" value="Следующий >>" name="next_query"' + \
           (' disabled' if query.ordernum <= 0 else '') + \
           '>'


def render_pause_button(query):
    # TODO проверить, что можно сохранять промежуточные результаты
    return '<input type="submit" value="Прервать" name="pause_query">'


def render_exit_button(query):
    # TODO проверить, что на все вопросы получены ответы
    return '<input type="submit" value="Завершить" name="exit_query">'


def render_reset(query):
    # TODO проверить условия тестирования на возможность изменить уже сохранённый ответ
    return '<input type="submit" value="Очистить" name="clear_query">'

def get_result_form(query):
    if query.question.qtype == RADIOBUTTON:
        return

def show_query(request, queryid):
    # TODO
    # TODO
    # TODO
    # TODO
    # TODO
    query = get_object_or_404(Anketa, pk=queryid)
    maxquerynum = Anketa.objects.all().filter(attempt=query.attempt).aggregate(Max('ordernum'))
    form = get_result_form(query)
    return render(
        request,
        'showquery.html',
        {
            'query': query,
            'maxquerynum': maxquerynum,
            'form': form,
            # 'prev_query': render_prev_query_button(query),
            # 'pause_query': render_pause_button(query),
            # 'exit_query': render_exit_button(query),
            # 'next_query': render_next_query_button(query),
        }
    )

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
