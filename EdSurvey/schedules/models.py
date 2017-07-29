from django.db import models
from querylists.models import QueryList


class Task(models.Model):
    """ Задачи на тестирование
    Задача поставлена группой учителей группе студентов в рамках определённой организации.
    Задание ограничено количеством попыток.
    """
    # teachers = models.ForeignKey('auth.group')
    # students = models.ForeignKey('auth.group')
    # organization = models.ForeignKey(Organization)
    querylist = models.ForeignKey(QueryList)
    attempts = models.PositiveIntegerField(default=1)
    description = models.CharField(max_length=30)
    # status = models.SmallIntegerField()

    class Meta:
        verbose_name = 'Задание на тестирование'
        verbose_name_plural = 'Задания на тестирование'

    def __str__(self):
        return "{}({})".format(self.description, self.querylist.name)


class Schedule(models.Model):
    """ Расписание задач """
    task = models.ForeignKey(Task)
    start = models.DateTimeField()
    finish = models.DateTimeField()
    description = models.CharField(max_length=30, blank=True, null=True)
    # status = models.SmallIntegerField()

    class Meta:
        verbose_name = 'Назначеное тестирование'
        verbose_name_plural = 'Расписание заданий'

    def __str__(self):
        return "{} {}".format(self.task.description, self.description)
