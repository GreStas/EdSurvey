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
    :return: void
    """
    if attempt.finished:
        raise AttemptError("попытыка уже закрыта")
    elif now() < attempt.schedule.start:
        raise ScheduleError("срок расписания ещё не наступил")
    elif now() > attempt.schedule.finish:
        raise ScheduleError("срок расписания уже завершился")


def err_results(query):
    """ Проверка, что на вопрос дан ответ
    RB - есть единственный ответ
    CB - есть хотя-бы один ответ
    LL - для всех подвопросов выбран вариант и варианты уникальные

    :param query: Anketa
    :return: errstr or None
    """
    # Для простых вопросов (RB и CB) проверяем, что есть хотя-бы один ответ
    cnt = Result.objects.all().filter(anketa=query).count()
    qtype = query.question.qtype
    if qtype == RADIOBUTTON and cnt != 1:
        return "Для вопроса {} должен быть единственный ответ ({}).".format(query, cnt,)
    elif qtype == CHECKBOX and cnt == 0:
        return "Для вопроса {} должен быть хотя-бы один ответ ({}).".format(query, cnt,)
    elif qtype in (LINKEDLISTS):
        # Сколько должно быть ответов?
        answers_cnt = Answer.objects.all().filter(
            question=query.question
        ).count()
        # Сколько получено вариантов?
        results_cnt = ResultLL.objects.all().filter(
            anketa=query,
            choice__isnull=False,
        ).count()
        if answers_cnt != results_cnt:
            return "Для вопроса {} должны быть заполены все варианты ({}).".format(query, answers_cnt,)
        # проверим,что есть все варианты
        answers = set([a.id for a in Answer.objects.all().filter(question=query.question)])
        results = set([r.choice.id for r in ResultLL.objects.all().filter(anketa=query, choice__isnull=False)])
        print('Answers:', answers)
        print('Results:', results)
        if answers - results:
            return "Для вопроса '{}' каждый вариант ответа может быть использован только один раз.".format(query.question.name,)
    return ''


def finish_attempt(request, attemptid):
    """ Финализация попытки
     Проверяет, что на все вопросы получены ответы.
     Записывает finished=now()
    """
    errors = False
    attempt = get_object_or_404(Attempt, pk=attemptid)
    for query in Anketa.objects.all().filter(attempt=attempt):
        errmsg = err_results(query)
        if errmsg:
            errors = True
            messages.add_message(request, messages.INFO, errmsg)
    if errors:
        # Если была хоть какая-то ошибка, то вернуться обратно на прохождение опроса
        return redirect(reverse(
            # 'surveys:showquery', args=[Anketa.objects.all().get(attempt=attempt, ordernum=1).id]
            'surveys:runattempt', args=[attemptid],
        ))
    if attempt.schedule.task.autoclose:
        attempt.finished=now()
        attempt.save()
    return redirect(reverse(
        'surveys:closeattempt',
        args=[attemptid]
    ))


def generate_anketa(attempt):
    """ Генерирует последовательность Result """
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
    """ Задать следующий возможный вопрос
    или завершить попытку
    или предложить завершить попытку
    """
    attempt = get_object_or_404(Attempt, pk=attemptid)
    if not attempt.schedule.task.viewable:
        try:
            validate_modify_attempt(attempt)
        except (AttemptError, ScheduleError) as e:
            raise ValidationError("Невозможно использовать эту поптыку, так как {}".format(e))
    # Факт: доступные попытки ещё есть.
    # Ищем query
    query = None
    if Anketa.objects.all().filter(attempt=attempt).count() == 0:
        # Для новой попытки - сгенерировать анкету:
        generate_anketa(attempt)
        query = Anketa.objects.get(attempt=attempt, ordernum=1)
    else:
        # Продолжение открытой попытки у которой точно уже сформированы вопросы в Anketa.
        # вычислить первый_неотвеченный_вопрос открытой поптыки
        query_1st = None
        for anketa in Anketa.objects.all().filter(attempt=attempt).order_by('ordernum'):
            if err_results(anketa):
                query_1st = anketa
                break
        if attempt.schedule.task.editable or attempt.schedule.task.viewable:
            if query_1st:
                query = query_1st
            else:
                query = Anketa.objects.get(attempt=attempt, ordernum=1)
        else:
            query = query_1st
    if query:
        # Продолжить опрос с найденого в Anketa вопроса
        return redirect(reverse('surveys:showquery', args=[query.id]))
    # Нет вопросов на которые ещё можно ответить
    elif attempt.schedule.task.autoclose:
        # Автоматически закрыть попытку
        return redirect(reverse('surveys:finishattempt', args=[attemptid]))
    else:
        # Страница с подтверждением закрытия попытки
        return redirect(reverse(
            'surveys:closeattempt',
            args=[attemptid]
        ))


def close_attempt(request, attemptid):
    attempt = get_object_or_404(Attempt, pk=attemptid)
    readonly = False
    try:
        validate_modify_attempt(attempt)
    except (AttemptError, ScheduleError) as e:
        readonly = attempt.schedule.task.viewable

    # Обработка формы
    if request.POST.get("return"):
        return redirect(reverse(
            'surveys:runattempt',
            args=[attempt.id]
        ))
    elif request.POST.get("finish") and not readonly:
        attempt.finished = now()
        attempt.save()
        return redirect(reverse(
            'schedules:scheduleinfo',
            args=[attempt.schedule.id]
        ))
    # Страница
    answered_cnt = 0
    waited_cnt = 0
    for anketa in Anketa.objects.all().filter(attempt=attempt).order_by('ordernum'):
        if err_results(anketa):
            waited_cnt += 1
        else:
            answered_cnt += 1
    return render(
        request,
        'closeattempt.html',
        {
            'attempt': attempt,
            'answered_cnt': answered_cnt,
            'waited_cnt': waited_cnt,
            'readonly': readonly,
        }
    )


def get_answer_contents(answer_model, question):
    """ Формирует перечень вариантов ответов - list(answer_model objects) """
    ordered_contents = [query for query in
                        answer_model.objects.all().filter(question=question, ordernum__isnull=False).order_by('ordernum')]
    unordered_contents = [query for query in
                          answer_model.objects.all().filter(question=question, ordernum__isnull=True)]
    shuffle(unordered_contents)
    return ordered_contents + unordered_contents


def is_readonly(query):
    # Validate access
    editable = query.attempt.schedule.task.editable
    viewable = query.attempt.schedule.task.viewable
    has_errs = err_results(query)
    if not editable and not has_errs:
        if viewable:
            return True
        else:
            raise ObjectDoesNotExist
    else:
        return False

def render_result_form(request, query):
    readonly = is_readonly(query)
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
                'readonly': readonly,
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
                'readonly': readonly,
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
                'readonly': readonly,
            },
        )


def save_result(query, request):
    """ Сохраняет данные из формы без проверки валидности данных на форме """
    if is_readonly(query):
        return

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


def get_prev_query_ordernum(query):
    num = query.ordernum-1
    value = None
    if num > 0:
        if query.attempt.schedule.task.editable or query.attempt.schedule.task.viewable:
            value = num
        else:
            # Ищем ближайший вопрос на который не был дан корректный ответ
            for prev_query in Anketa.objects.all().filter(attempt=query.attempt,
                                                      ordernum__lte=num).order_by('-ordernum'):
                if err_results(prev_query):
                    value = prev_query.ordernum
                    break
    return value


def get_next_query_ordernum(query):
    num = query.ordernum + 1
    maxquerynum = Anketa.objects.all().filter(attempt=query.attempt).aggregate(Max('ordernum'))['ordernum__max']
    value = None
    if num <= maxquerynum:
        if query.attempt.schedule.task.editable or query.attempt.schedule.task.viewable:
            value = num
        else:
            # Ищем ближайший вопрос на который не был дан корректный ответ
            for next_query in Anketa.objects.all().filter(attempt=query.attempt,
                                                      ordernum__gte=num).order_by('ordernum'):
                if err_results(next_query):
                    value = next_query.ordernum
                    break
    return value


def show_query(request, queryid):
    query = get_object_or_404(Anketa, pk=queryid)
    maxquerynum = Anketa.objects.all().filter(attempt=query.attempt).aggregate(Max('ordernum'))['ordernum__max']
    prev_ordernum = get_prev_query_ordernum(query)
    next_ordernum = get_next_query_ordernum(query)

    form = render_result_form(request, query)

    if request.POST.get("prev_query"):
        save_result(query, request)
        if prev_ordernum:
            return redirect(reverse(
                'surveys:showquery',
                args=[get_object_or_404(Anketa, attempt=query.attempt, ordernum=prev_ordernum).id])
            )
    elif request.POST.get("next_query"):
        save_result(query, request)
        if next_ordernum:
            return redirect(reverse(
                'surveys:showquery',
                args=[get_object_or_404(Anketa, attempt=query.attempt, ordernum=next_ordernum).id])
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
            'prevordernum': prev_ordernum,
            'nextordernum': next_ordernum,
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
