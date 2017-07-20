from django.db import models
from questions.models import Question


class TestCase(models.Model):
    class Meta:
        verbose_name = 'Тест-кейс'
        verbose_name_plural = 'Тест-кейсы'

    def __str__(self):
        return "{}.{}".format(self.id, self.name)

    name = models.CharField(max_length=64)
    description = models.TextField
    # status = models.IntegerField(null=True)
    # authors = models.ForeignKey('auth.User')
    # params xml


class TestContent(models.Model):
    class Meta:
        verbose_name = 'Состав Тест-кейса'
        verbose_name_plural = verbose_name
        unique_together = ('testcase', 'question')

    def __str__(self):
        return "{}-{}".format(self.testcase, self.question)

    testcase = models.ForeignKey(TestCase)
    question = models.ForeignKey(Question)
    ordernum = models.PositiveIntegerField(null=True, blank=True)
    # status = models.IntegerField(null=True)