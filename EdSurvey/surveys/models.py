from django.core.exceptions import ValidationError
from django.db import models
from questions.models import Question, AnswerRB, AnswerCB, AnswerLL
from schedules.models import Task, Schedule


class Attempt(models.Model):
    """ Попытки сдать тест-кейс """
    class Meta:
        verbose_name = 'Попытка сдать тест-кейс'
        verbose_name_plural = 'Попытки сдать тест-кейс'
        # unique_together = ('user', schedule', 'attempt')
        unique_together = ('schedule', 'attempt')

    def __str__(self):
        return "#{}.{}".format(str(self.started), str(self.schedule))

    # user = models.ForeignKey('auth.user')
    schedule = models.ForeignKey(Schedule)
    attempt = models.PositiveIntegerField(null=True)
    started = models.DateTimeField()    # not null, now(), noeditable
    finished = models.DateTimeField(blank=True, null=True)   # null, noeditable
    # status = models.SmallIntegerField()


class Result(models.Model):
    """ Ответы пользователей на анкеты """
    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
        # unique_together = ('user', 'attempt', 'question')
        # unique_together = ('attempt', 'question')

    def __str__(self):
        return "#{}.{}".format(self.attempt, str(self.question))

    # user = models.ForeignKey('auth.user') # Пользоватеь
    attempt = models.ForeignKey(Attempt)    #   в ходе попытки
    question = models.ForeignKey(Question)  #     на вопрос
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    # status = models.SmallIntegerField()


class ResultRB(Result):
    """ qtype == CB
        необходим для создания отдельных валидаторов
    """
    class Meta:
        verbose_name = 'Одиночный Ответ (RadioButton)'
        verbose_name_plural = 'Одиночные Ответы (RadioButton)'

    result_ptr = models.OneToOneField(
        Result, on_delete=models.CASCADE,
        parent_link=True,
    )
    answerRB = models.ForeignKey(AnswerRB)  #       дал ответ

    def clean(self):
        qtype = self.question.qtype
        if qtype != 'RB':
            raise ValidationError("Тип вопроса ({}) и тип ответа (RB) не совпадают.".format(qtype))


class ResultCB(Result):
    """ qtype == CB
        необходим для создания отдельных валидаторов
    """
    class Meta:
        verbose_name = 'Множественный Ответ (CheckBox)'
        verbose_name_plural = 'Множественные Ответы (CheckBox)'

    result_ptr = models.OneToOneField(
        Result, on_delete=models.CASCADE,
        parent_link=True,
    )
    answerCB = models.ForeignKey(AnswerCB)  #       дал ответ

    def clean(self):
        qtype = self.question.qtype
        if qtype != 'CB':
            raise ValidationError("Тип вопроса ({}) и тип ответа (CB) не совпадают.".format(qtype))


class ResultLL(Result):
    class Meta:
        verbose_name = 'Ответ-Путанка'
        verbose_name_plural = 'Ответы-Путанки'

    result_ptr = models.OneToOneField(
        Result, on_delete=models.CASCADE,
        parent_link=True,
    )
    answerLL = models.ForeignKey(AnswerLL)  #       дал ответ
    itemLL = models.ForeignKey(AnswerLL, related_name='+')    #         выбрав вариант

    def clean(self):
        qtype = self.question.qtype
        if qtype != 'LL':
            raise ValidationError("Тип вопроса ({}) и тип ответа (LL) не совпадают.".format(qtype))
