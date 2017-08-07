from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.utils.timezone import now

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
    querylist = models.ForeignKey(QueryList, on_delete=models.PROTECT)
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
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    start = models.DateTimeField()
    finish = models.DateTimeField()
    description = models.CharField(max_length=30, blank=True, null=True)
    # status = models.SmallIntegerField()

    class Meta:
        verbose_name = 'Назначеное тестирование'
        verbose_name_plural = 'Расписание заданий'

    def __str__(self):
        return "{} {}".format(self.task.description, self.description)

def schedule_pre_save(instance, **kwargs):
    """ Validation
    - Нельзя менять расписание, если по нему уже есть начатые попытки.
    """
    if Schedule.objects.all().filter(pk=instance.id).count() > 0:
        if Attempt.objects.all().filter(schedule=instance).count() > 0:
            raise ValidationError("Нельзя изменять расписание, если по нему уже есть начатые попытки.")

pre_save.connect(schedule_pre_save, sender=Schedule)


class Attempt(models.Model):
    """ Попытки сдать тест-кейс """
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT)
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


# Cross-Models Validations

def task_pre_save(instance, **kwargs):
    """ Validation
    - Нельзя изменять Задание, если по нему уже существует расписание.
    """
    if Task.objects.all().filter(pk=instance.id).count() > 0:
        if Schedule.objects.all().filter(task=instance).count() > 0:
            raise ValidationError("Нельзя изменять задание, если по нему уже существует расписание.")

pre_save.connect(task_pre_save, sender=Task)
