# surveys.views
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
from django.db.models.aggregates import Max
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls.base import reverse
from django.utils.timezone import now
from django.db import transaction
from django.contrib import messages

from random import shuffle

from .models import Anketa, Result, ResultLL  # , ResultRB, ResultCB
from schedules.models import Schedule, Task, Attempt
from querylists.models import QueryContent
from questions.models import RADIOBUTTON, CHECKBOX, LINKEDLISTS, Question, Answer, AnswerRB, AnswerCB, AnswerLL


class AttemptError(RuntimeError):
    pass


class ScheduleError(RuntimeError):
    pass


def validate_modify_attempt(attempt):
    """ Валидация - нельзя вносить изменения в объекты,
    которые ссылаются на попытку, если:
    - попытыка закрыта
    - не в сроках расписания

    :param attempt: sueveys.models.Attempt
    :return:
    """
    if attempt.finished:
        raise AttemptError("попытыка уже закрыта")
    elif now() < attempt.schedule.start:
        raise ScheduleError("срок расписания ещё не наступил")
    elif now() > attempt.schedule.finish:
        raise ScheduleError("срок расписания уже завершился")
    # print('instance.id=', instance.id)
    # try:
    #     result = Result.objects.get(pk=instance.id)
    #     print('result.id=', result.id)
    # except ObjectDoesNotExist:
    #     result = None
    # if result:  # update
    #     print('result.anketa.attempt.finished',result.anketa.attempt.finished)
    #     print('result.anketa.attempt.schedule.start',result.anketa.attempt.schedule.start)
    #     print(now())
    #     print('result.anketa.attempt.schedule.finish',result.anketa.attempt.schedule.finish)
    #     if result.anketa.attempt.finished:
    #         ValidationError("Нельзя вносить изменения, если попытыка уже закрыта.")
    #     elif now() < result.anketa.attempt.schedule.start:
    #         ValidationError("Срок расписания ещё не наступил.")
    #     elif now() > result.anketa.attempt.schedule.finish:
    #         ValidationError("Срок расписания уже завершился.")
    # else:  # insert
    #     print('instance.anketa.attempt.schedule.start',instance.anketa.attempt.schedule.start)
    #     print('instance.anketa.attempt.schedule.finish',instance.anketa.attempt.schedule.finish)
    #     if now() < instance.anketa.attempt.schedule.start:
    #         ValidationError("Срок расписания ещё не наступил.")
    #     elif now() > instance.anketa.attempt.schedule.finish:
    #         ValidationError("Срок расписания уже завершился.")


def finish_attempt(request, attemptid):
    """ Финализация попытки
     Проверяет, что на все вопросы получены ответы.
     Записывает finished=now()
    """
    errors = False
    attempt = get_object_or_404(Attempt, pk=attemptid)
    for query in Anketa.objects.all().filter(attempt=attempt):
        # Для простых вопросов (RB и CB) проверяем, что есть хотя-бы один ответ
        cnt = Result.objects.all().filter(anketa=query).count()
        qtype = query.question.qtype
        if qtype == RADIOBUTTON and cnt != 1:
            errors = True
            messages.add_message(
                request,
                messages.INFO,
                "Для вопроса {} должен быть единственный ответ ({}).".format(
                    query,
                    cnt,
                )
            )
        elif qtype == CHECKBOX and cnt == 0:
            errors = True
            messages.add_message(
                request,
                messages.INFO,
                "Для вопроса {} должен быть хотя-бы один ответ ({}).".format(
                    query,
                    cnt,
                )
            )
        elif qtype in (LINKEDLISTS):
            # Сколько должно быть ответов?
            answers_cnt = Answer.objects.all().filter(question=query.question).count()
            results_cnt = ResultLL.objects.all().filter(
                anketa=query,
                choice__isnull=False,
            ).count()
            if answers_cnt != results_cnt:
                errors = True
                messages.add_message(
                    request,
                    messages.INFO,
                    "Для вопроса {} должны быть заполены все варианты ({}).".format(
                        query,
                        answers_cnt,
                    )
                )
    # Если была хоть какая-то ошибка, то вернуться обратно на showquery
    if errors:
        print(messages.get_messages(request))
        # TODO вернуться обратно на showquery
        return show_query(
            request,
            queryid=Anketa.objects.all().get(attempt=attempt, ordernum=1).id,
        )
    attempt.finished=now()
    attempt.save()
    # TODO Вернуться на описание задания в расписании
    return redirect(reverse(
        'schedules:scheduleinfo',
        args=[attempt.schedule.id]
    ))


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
    try:
        validate_modify_attempt(attempt)
    except (AttemptError, ScheduleError) as e:
        raise ValidationError("Невозможно создать анкету для данного опроса так как {}".format(e))
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
                ordernum=i+1,
            )
            a.save()


def run_attempt(request, attemptid):
    attempt = get_object_or_404(Attempt, pk=attemptid)
    try:
        validate_modify_attempt(attempt)
    except (AttemptError, ScheduleError) as e:
        raise ValidationError("Невозможно использовать эту поптыку, так как {}".format(e))
    if Anketa.objects.all().filter(attempt=attempt).count() == 0:
        generate_anketa(attempt)
    query = get_object_or_404(Anketa, attempt=attempt, ordernum=1)
    return redirect(reverse('surveys:showquery', args=[query.id]))


def get_answer_contents(answer_model, question):
    """ Формирует перечень вариантов ответов - list(answer_model objects) """
    ordered_contents = [query for query in
                        answer_model.objects.all().filter(question=question, ordernum__isnull=False).order_by('ordernum')]
    unordered_contents = [query for query in
                          answer_model.objects.all().filter(question=question, ordernum__isnull=True)]
    shuffle(unordered_contents)
    return ordered_contents + unordered_contents


def render_result_form(request, query):
    tooltip = None

    if query.question.qtype == RADIOBUTTON:
        contents = get_answer_contents(AnswerRB, query.question)
        # Вычитать ранее полученный результат, если его нет, то вернуть None
        try:
            result = Result.objects.get(anketa=query).answer.id
        except ObjectDoesNotExist:
            result = None
        except MultipleObjectsReturned:
            # Жёстко удаляем всю халтуру! RB должен быть один!!!
            result = None
            Result.objects.all().filter(anketa=query).delete()
        if result is None:
            tooltip = "Вам необходимо выбрать один единственный обязательный ответ."
        return render_to_string(
            'resultrbblock.html',
            {
                'contents': contents,
                'result': result,
                'tooltip': tooltip,
            },
        )

    elif query.question.qtype == CHECKBOX:
        contents = get_answer_contents(AnswerCB, query.question)
        data = []
        empty = True
        for content in contents:
            # Вычитать ранее полученный результат, если его нет, то вернуть None
            try:
                result = Result.objects.get(anketa=query, answer=content.answer_ptr).answer.id
                empty = False
            except ObjectDoesNotExist:
                result = None
            except MultipleObjectsReturned:
                # Жёстко удаляем всю халтуру!
                Result.objects.all().filter(anketa=query, answer=content.answer_ptr).delete()
            data.append((content,result))
        if empty:
            tooltip = "Вам необходимо выбрать хотя-бы один ответ."
        return render_to_string(
            'resultcbblock.html',
            {
                # 'contents': contents,
                'data': data,
                'tooltip': tooltip,
            },
        )

    elif query.question.qtype == LINKEDLISTS:
        # Формируем перечень вопросов в паутинке
        contents = get_answer_contents(AnswerLL, query.question)
        # Формируем перечень ответов в паутинке
        # answers = get_answer_contents(AnswerLL, query.question)
        answers = contents.copy()
        shuffle(answers)

        cnt = len(answers)
        cntlen = len(str(cnt))
        data = []
        for i in range(cnt):
            content, answer = contents[i], answers[i]
            # Вычитать ранее полученный результат, если его нет, то вернуть None
            value = None
            try:
                result = ResultLL.objects.get(anketa=query, answer=content.answer_ptr)  #.answer.id
                # Если ранее уже давался ответ, то Result.choice уже его хранит
                # Найти номер соответсвующего ответа в answers
                for j in range(cnt):
                    # print(answers[j].id, result.choice.id)
                    if answers[j] == result.choice:
                        value = j+1
                        break
            except ObjectDoesNotExist:
                pass    # value = None
            except MultipleObjectsReturned:
                # # Жёстко удаляем всю халтуру!
                # ResultLL.objects.all().filter(anketa=query, answer=content.answer_ptr).delete()
                pass    # value = None
            data.append((content, answer, value))

        empty = False
        all_values = set([x+1 for x in range(cnt)])
        values = set()
        for (content, answer, value) in data:
            if value is None:
                empty = True
            else:
                values.add(value)

        if empty:
            tooltip = "Необходимо заполнить все варианты."
        elif len(all_values) != len(values):
            tooltip = "Каждый вариант можно использовать только один раз - повторения недопустимы."

        return render_to_string(
            'resultllblock.html',
            {
                'data': data,
                'cnt': cnt,
                'cntlen': cntlen,
                'tooltip': tooltip,
            },
        )


def save_result(query, request):
    """ Сохраняет данные из формы без проверки валидности данных на форме """
    try:
        validate_modify_attempt(query.attempt)
    except (AttemptError, ScheduleError) as e:
        raise ValidationError("Ваш ответ не принят так как {}".format(e))

    if query.question.qtype == RADIOBUTTON:
        choice = request.POST.get('choice')
        # print('choice=', choice)
        if choice:
            answer = get_object_or_404(Answer, pk=int(request.POST.get('choice')))
            # Найти уже существующй ответ и внести в него правку, если необходимо
            try:
                result = Result.objects.get(anketa=query)
                if result.answer != answer:
                    result.answer = answer
            except ObjectDoesNotExist:
                # Так как ответа ранее не было, то создать новый ответ
                result = Result(
                    anketa=query,
                    answer=answer,
                )
            result.save()
        else:
            Result.objects.all().filter(anketa=query).delete()

    elif query.question.qtype == CHECKBOX:
        choices = [int(c) for c in request.POST.getlist('choice')]
        # Зачистим те, которые не выбраны в этот раз
        for result in Result.objects.all().filter(anketa=query):
            if result.id not in choices:
                result.delete()
        for answerid in choices:   # answerid - это AnswerCB.id
            try:
                result = Result.objects.get(anketa=query, answer_id=answerid)
            except ObjectDoesNotExist:
                # Такого ответа ранее не было, то создать новый ответ
                result = Result(
                    anketa=query,
                    answer=get_object_or_404(AnswerCB, pk=answerid)
                )
                result.save()

    elif query.question.qtype == LINKEDLISTS:
        cnt = int(request.POST.get('cnt'))
        contents = []
        means = []
        answers = []
        # Воссоздаём значения в форме
        for i in range(cnt):
            forloop_count = str(i+1)    # Because forloop.counter starts from 1
            contents.append(int(request.POST.get('content{}'.format(forloop_count))))
            answers.append(int(request.POST.get('answer{}'.format(forloop_count))))
            mean = request.POST.get('choice{}'.format(forloop_count))
            if mean:
                means.append(int(mean)-1)   # Because forloop.counter starts from 1
            else:
                means.append(None)
            # print('({}) content, mean, answer = {}, {}, {}'.format(forloop_count, contents[i], means[i], answers[i]))

        # Проходим по таблице
        # print('Проходим по таблице')
        for i in range(cnt):
            # print('({}) content, mean, answer = {}, {}, {}'.format(i, contents[i], means[i], answers[i]))
            if means[i] is not None:
                answer = get_object_or_404(Answer, pk=contents[i])
                choice = get_object_or_404(AnswerLL, pk=answers[means[i]])
                try:
                    result = ResultLL.objects.get(anketa=query, answer=answer)
                    if result.choice.id != choice.id:
                        result.choice = choice
                        result.save()
                except ObjectDoesNotExist:
                    result = ResultLL(anketa=query, answer=answer, choice=choice)
                    result.save()
            else:
                # Если ничего не введено, то стереть такие результаты
                ResultLL.objects.all().filter(anketa=query, answer=contents[i]).delete()


def show_query(request, queryid):
    query = get_object_or_404(Anketa, pk=queryid)
    maxquerynum = Anketa.objects.all().filter(attempt=query.attempt).aggregate(Max('ordernum'))['ordernum__max']

    form = render_result_form(request, query)

    if request.POST.get("prev_query"):
        save_result(query, request)
        return redirect(reverse(
            'surveys:showquery',
            args=[get_object_or_404(Anketa, attempt=query.attempt, ordernum=query.ordernum-1).id])
        )
    elif request.POST.get("next_query"):
        save_result(query, request)
        return redirect(reverse(
            'surveys:showquery',
            args=[get_object_or_404(Anketa, attempt=query.attempt, ordernum=query.ordernum+1).id])
        )
    elif request.POST.get("exit_query"):
        save_result(query, request)
        return redirect(reverse(
            'surveys:finishattempt',
            args=[query.attempt.id]
        ))
    elif request.POST.get("pause_query"):
        save_result(query, request)
        return redirect(reverse(
            'schedules:scheduleinfo',
            args=[query.attempt.schedule.id]
        ))

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


# def render_prev_query_button(query):
#     return render_to_string(
#         '<input type="submit" value="<< Предыдущий" name="prev_query"' + \
#         (' disabled' if query.ordernum <= 0 else '') + \
#         '>'
#     )
#
#
# def render_next_query_button(query):
#     return '<input type="submit" value="Следующий >>" name="next_query"' + \
#            (' disabled' if query.ordernum <= 0 else '') + \
#            '>'
#
#
# def render_pause_button(query):
#     # TODO проверить, что можно сохранять промежуточные результаты
#     return '<input type="submit" value="Прервать" name="pause_query">'
#
#
# def render_exit_button(query):
#     # TODO проверить, что на все вопросы получены ответы
#     return '<input type="submit" value="Завершить" name="exit_query">'
#
#
# def render_reset(query):
#     # TODO проверить условия тестирования на возможность изменить уже сохранённый ответ
#     return '<input type="submit" value="Очистить" name="clear_query">'
