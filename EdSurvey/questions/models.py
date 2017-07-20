from django.db import models


class Question(models.Model):
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return "{}.{}.{}".format(self.id, self.qtype, self.description[:15])

    RADIOBUTTON = 'RB'  # (*) One -from- List
    CHECKBOX = 'CB'     # [v] Some -from- List
    LINKEDLISTS = 'LL'   # Link One from first list -to- One from other list
    QUESTION_TYPE_CHOICES = (
        (RADIOBUTTON, 'Один из ...'),
        (CHECKBOX, 'Несколько из ...'),
        (LINKEDLISTS, "Путанка"),
    )

    qtype = models.CharField(
        max_length=2,
        choices=QUESTION_TYPE_CHOICES,
        default=RADIOBUTTON,
    )

    description = models.TextField()
    # status = models.IntegerField(null=True)

    # content = models.XML - Как лучше хранить форматированный текст?

    # organisation = models.ForeignKey('organisations.organisation')
    # authors = models.ForeignKey('auth.User')


class Answer(models.Model):
    class Meta:
        verbose_name = 'Простой Ответ'
        verbose_name_plural = 'Простые Ответы'

    question = models.ForeignKey('Question')
    content = models.TextField()
    ordernum = models.PositiveIntegerField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    # status = models.IntegerField(null=True)


class AnswerLL(models.Model):
    class Meta:
        verbose_name = 'Ответ-Путанка'
        verbose_name_plural = 'Ответы-Путанки'

    question = models.ForeignKey('Question')
    content1 = models.TextField()
    content2 = models.TextField()
    ordernum1 = models.PositiveIntegerField(null=True, blank=True)
    ordernum2 = models.PositiveIntegerField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    # status = models.IntegerField(null=True)
