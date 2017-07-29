from django.db import models

from questions.models import Question


class QueryList(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    # status = models.IntegerField(null=True)
    # authors = models.ForeignKey('auth.User')
    # params xml

    class Meta:
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'

    def __str__(self):
        return "{}.{}".format(self.id, self.name)


class QueryContent(models.Model):
    querylist = models.ForeignKey(QueryList)
    question = models.ForeignKey(Question)
    ordernum = models.PositiveIntegerField(null=True, blank=True)
    # status = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Состав Анкеты'
        verbose_name_plural = 'Состав Анкет'
        unique_together = ('querylist', 'question')

    def __str__(self):
        return "{}-{}".format(self.querylist, self.question)