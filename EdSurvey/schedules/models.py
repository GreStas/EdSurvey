from django.db import models
from questions.models import Question


class Task(models.Model):
    """ Задачи на тестирование
    У каждой задачи есть группа авторов и группа студентов.
    Задача может быть поставлена в рамках конкретной организации
    """
    # teachers = models.ForeignKey('auth.group')
    # students = models.ForeignKey('auth.group')
    # organization = models.ForeignKey(Organization)
    testcase = models.ForeignKey(Question)
    attempts = models.PositiveIntegerField(default=1)
    # status = models.SmallIntegerField()


class Schedule(models.Model):
    """ Расписание задач """
    task = models.ForeignKey(Task)
    start = models.DateTimeField()
    finish = models.DateTimeField()
    # status = models.SmallIntegerField()
