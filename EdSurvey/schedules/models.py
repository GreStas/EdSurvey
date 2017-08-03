from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models.signals import pre_save

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


class Attempt(models.Model):
    """ Попытки сдать тест-кейс """
    schedule = models.ForeignKey(Schedule)
    started = models.DateTimeField(auto_now_add=True, auto_now=False)
    finished = models.DateTimeField(blank=True, null=True)
    # user = models.ForeignKey('auth.user')
    # status = models.SmallIntegerField()

    class Meta:
        verbose_name = 'Попытка пройти тест'
        verbose_name_plural = 'Попытки пройти тест'

    def __str__(self):
        return "#{}.{}".format(str(self.started), str(self.schedule))


def attempt_pre_save(instance, **kwargs):
    try:
        # opened_attempt =
        Attempt.objects.get(
            schedule=instance.schedule,
            finished__isnull=True,
        )
    except ObjectDoesNotExist:
        # Открытых попыток нет.
        return
    try:
        # считываем предыдущее состояние
        attempt = Attempt.objects.get(pk=instance.id)
    except ObjectDoesNotExist:
        # Создаётся новая попытка, но есть opened_attempt
        raise ValidationError("Нельзя сделать новую попытку пока существует незавершённая.")

    # Проверяем на внесение изменений
    if attempt.finished:
        raise ValidationError("Нельзя вносить изменения в завершённую попытку.")
    elif instance.started > instance.finished:
        raise ValidationError("Дата завершения должна быть позже даты начала.")




pre_save.connect(attempt_pre_save, sender=Attempt)
