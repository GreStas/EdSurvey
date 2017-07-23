from django.db import models
from testcases.models import TestCase


class Task(models.Model):
    """ Задачи на тестирование
    У каждой задачи есть группа авторов и группа студентов.
    Задача может быть поставлена в рамках конкретной организации
    """
    class Meta:
        verbose_name = 'Задание на тестирование'
        verbose_name_plural = 'Задания на тестирование'

    def __str__(self):
        return "{}({})".format(self.description, self.testcase.name)

    # teachers = models.ForeignKey('auth.group')
    # students = models.ForeignKey('auth.group')
    # organization = models.ForeignKey(Organization)
    testcase = models.ForeignKey(TestCase)
    attempts = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=30)
    # status = models.SmallIntegerField()


class Schedule(models.Model):
    """ Расписание задач """
    class Meta:
        verbose_name = 'Назначеное тестирование'
        verbose_name_plural = 'Расписание заданий'

    def __str__(self):
        return "{} {}".format(self.task.description, self.description)

    task = models.ForeignKey(Task)
    start = models.DateTimeField()
    finish = models.DateTimeField()
    description = models.CharField(max_length=30, blank=True, null=True)
    # status = models.SmallIntegerField()
