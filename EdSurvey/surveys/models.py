from django.core.exceptions import ValidationError
from django.db import models

from questions.models import Question, AnswerRB, AnswerCB, AnswerLL
from schedules.models import Attempt


class Result(models.Model):
    """ Ответы пользователей на анкеты """
    # user = models.ForeignKey('auth.user') # Пользоватеь
    attempt = models.ForeignKey(Attempt)    #   в ходе попытки
    question = models.ForeignKey(Question)  #     на вопрос
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    ordernum = models.PositiveIntegerField()    # Номер под которым задаётся вопрос.
    # status = models.SmallIntegerField()

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
        # unique_together = ('user', 'attempt', 'question')
        # unique_together = ('attempt', 'question')

    def __str__(self):
        return "#{}.{}".format(self.attempt, str(self.question))


class ResultRB(Result):
    """ qtype == CB
        необходим для создания отдельных валидаторов
    """
    result_ptr = models.OneToOneField(
        Result, on_delete=models.CASCADE,
        parent_link=True,
    )
    answerRB = models.ForeignKey(AnswerRB)  #       дал ответ

    class Meta:
        verbose_name = 'Одиночный Ответ (RadioButton)'
        verbose_name_plural = 'Одиночные Ответы (RadioButton)'

    def clean(self):
        qtype = self.question.qtype
        if qtype != 'RB':
            raise ValidationError("Тип вопроса ({}) и тип ответа (RB) не совпадают.".format(qtype))


class ResultCB(Result):
    """ qtype == CB
        необходим для создания отдельных валидаторов
    """
    result_ptr = models.OneToOneField(
        Result, on_delete=models.CASCADE,
        parent_link=True,
    )
    answerCB = models.ForeignKey(AnswerCB)  #       дал ответ

    class Meta:
        verbose_name = 'Множественный Ответ (CheckBox)'
        verbose_name_plural = 'Множественные Ответы (CheckBox)'

    def clean(self):
        qtype = self.question.qtype
        if qtype != 'CB':
            raise ValidationError("Тип вопроса ({}) и тип ответа (CB) не совпадают.".format(qtype))


class ResultLL(Result):
    result_ptr = models.OneToOneField(
        Result, on_delete=models.CASCADE,
        parent_link=True,
    )
    answerLL = models.ForeignKey(AnswerLL)  #       дал ответ
    itemLL = models.ForeignKey(AnswerLL, related_name='+')    #         выбрав вариант

    class Meta:
        verbose_name = 'Ответ-Путанка'
        verbose_name_plural = 'Ответы-Путанки'

    def clean(self):
        qtype = self.question.qtype
        if qtype != 'LL':
            raise ValidationError("Тип вопроса ({}) и тип ответа (LL) не совпадают.".format(qtype))
