from django.core.exceptions import ValidationError
from django.db import models

from questions.models import Question, Answer, AnswerLL
from schedules.models import Attempt


class Anketa(models.Model):
    """ Сгенерированые вопросы анкеты """
    # user = models.ForeignKey('auth.user') # Пользоватеь
    attempt = models.ForeignKey(Attempt, on_delete=models.PROTECT)    #   в ходе попытки
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


class Result(models.Model):
    anketa = models.ForeignKey(Anketa, on_delete=models.PROTECT)
    answer = models.ForeignKey(Answer, on_delete=models.PROTECT)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

# TODO pre_save_Result - добавить проверку, что RB может по анкете быть только один.


class ResultLL(Result):
    result_ptr = models.OneToOneField(
        Result, on_delete=models.CASCADE,
        parent_link=True,
    )
    choice = models.ForeignKey(AnswerLL, on_delete=models.PROTECT)

    def __str__(self):
        return "id{}.anketa{}.answer{}.choice{}".format(self.result_ptr.id,
                                                        self.result_ptr.anketa.id,
                                                        self.result_ptr.answer.id,
                                                        self.choice.id)
