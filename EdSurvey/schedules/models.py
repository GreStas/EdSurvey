from django.db import models
from querylists.models import QueryList


class Task(models.Model):
    """ Задачи на тестирование
    Задача поставлена группой учителей группе студентов в рамках определённой организации.
    Задание ограничено количеством попыток.
    Если нельзя просматривать свои ответы, то
        нельзя перемещаться по списку вопросов
        нельзя просмотреть в архиве свои ответы
    Если нельзя редактировать свои ответы, то
        нельзя в незакрытой попытке изменять свои ответы
        нельзя пропускать вопросы, чтобы ответить потом
    """
    # teachers = models.ForeignKey('auth.group')
    # students = models.ForeignKey('auth.group')
    # organization = models.ForeignKey(Organization)
    querylist = models.ForeignKey(QueryList)
    attempts = models.PositiveIntegerField(default=1)
    viewable = models.BooleanField(default=False)   # можно-ли просматривать свои ответы
    editable = models.BooleanField(default=False)   # можно-ли редактировать уже данные ответы
    autoclose = models.BooleanField(default=True)   # автозакрытие поптыки когда есть ответы на все вопросы
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
