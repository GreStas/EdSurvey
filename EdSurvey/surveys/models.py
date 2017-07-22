from django.db import models
from questions.models import Question, Answer
from schedules.models import Task, Schedule


class Attempt(models.Model):
    """ Попытки здать тест-кейс """
    class Meta:
        #unique_together = ('user', schedule', 'attempt')
        unique_together = ('schedule', 'attempt')

    # user = models.ForeignKey('auth.user')
    schedule = models.ForeignKey(Schedule)
    attempt = models.PositiveIntegerField()
    started = models.DateTimeField()    # not null, now(), noeditable
    finished = models.DateTimeField()   # null, noeditable
    # status = models.SmallIntegerField()


class Results(models.Model):
    """ Ответы пользователей на анкеты """
    class Meta:
        #unique_together = ('user', 'attempt', 'question')
        unique_together = ('attempt', 'question')

    # user = models.ForeignKey('auth.user') # Пользоватеь
    attempt = models.ForeignKey(Attempt)    #   в ходе попытки
    question = models.ForeignKey(Question)  #     на вопрос
    answer = models.ForeignKey(Answer)      #       дал ответ
    timemark = models.DateTimeField()       #         Дата и Время
    # status = models.SmallIntegerField()
