from django.db import models
from questions.models import Question, Answer
from schedules.models import Task, Schedule


class Attempt(models.Model):
    """ Попытки сдать тест-кейс """
    class Meta:
        verbose_name = 'Попытка сдать тест-кейс'
        verbose_name_plural = 'Попытки сдать тест-кейс'
        # unique_together = ('user', schedule', 'attempt')
        unique_together = ('schedule', 'attempt')

    def __str__(self):
        return "#{}.{}".format(self.attempt, str(self.schedule))

    # user = models.ForeignKey('auth.user')
    schedule = models.ForeignKey(Schedule)
    attempt = models.PositiveIntegerField()
    started = models.DateTimeField()    # not null, now(), noeditable
    finished = models.DateTimeField(blank=True, null=True)   # null, noeditable
    # status = models.SmallIntegerField()


class Result(models.Model):
    """ Ответы пользователей на анкеты """
    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
        #unique_together = ('user', 'attempt', 'question')
        unique_together = ('attempt', 'question', 'answer')

    def __str__(self):
        return "#{}.{}".format(self.attempt, str(self.question))

    # user = models.ForeignKey('auth.user') # Пользоватеь
    attempt = models.ForeignKey(Attempt)    #   в ходе попытки
    question = models.ForeignKey(Question)  #     на вопрос
    answer = models.ForeignKey(Answer)      #       дал ответ
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    # status = models.SmallIntegerField()
