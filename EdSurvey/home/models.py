from django.db import models
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db.models.signals import pre_save, pre_delete

from querylists.models import QueryList, QueryContent
from schedules.models import Task

# Cross-Applucations Validations and Signals

def querylist_pre_save(instance, **kwargs):
    """ Validation
    - Нельзя изменять Анкету, если по нему уже существует Задание.
    """
    if QueryList.objects.all().filter(pk=instance.id).count() > 0:
        if Task.objects.all().filter(querylist=instance).count() > 0:
            raise ValidationError("Нельзя изменять Анкету, если по ней уже существует Задание.")

pre_save.connect(querylist_pre_save, sender=QueryList)


def querycontent_pre_save(instance, **kwargs):
    """ Validation
    - Нельзя изменять Анкету, если по ней уже существует Задание.
    - Нельзя добавлять в Анкету новое содержимое, если по ней уже существует Задание.
    """
    try:
        querycontent = QueryContent.objects.get(pk=instance.id)
    except ObjectDoesNotExist:
        querycontent = None
    tasks_cnt = Task.objects.all().filter(querylist=instance.querylist).count()
    if querycontent:
        if tasks_cnt > 0:
            raise ValidationError("Нельзя изменять состав Анкеты, если по ней уже существует Задание.")
    elif tasks_cnt > 0:
            raise ValidationError("Нельзя добавлять в Анкету новое содержимое, если по ней уже существует Задание.")

pre_save.connect(querycontent_pre_save, sender=QueryContent)
