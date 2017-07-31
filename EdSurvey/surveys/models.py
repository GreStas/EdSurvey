from django.core.exceptions import ValidationError
from django.db import models

from questions.models import Question, AnswerRB, AnswerCB, AnswerLL
from schedules.models import Attempt


class Anketa(models.Model):
    """ Сгенерированые вопросы анкеты """
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

