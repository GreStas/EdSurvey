from django.db import models

from questions.models import Question
from clients.models import Division


class QueryList(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    division = models.ForeignKey(Division, on_delete=models.PROTECT)
    public = models.BooleanField(default=False)
    # status = models.IntegerField(null=True)
    # authors = models.ForeignKey('auth.User')
    # params xml

    class Meta:
        verbose_name = 'Опросник'
        verbose_name_plural = 'Опросники'

    def __str__(self):
        return "{}.{}".format(self.id, self.name)


class QueryContent(models.Model):
    querylist = models.ForeignKey(QueryList, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    ordernum = models.PositiveIntegerField(null=True, blank=True)
    # status = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Наполнение опросника'
        verbose_name_plural = 'Наполнение опросников'
        unique_together = ('querylist', 'question')

    def __str__(self):
        return "{}-{}".format(self.querylist, self.question)