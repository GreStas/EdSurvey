from django.db import models

OWNER_NAME = 'Владелец сайта'
OWNER_SHORTNAME = 'OWNER'

class Client(models.Model):
    name = models.CharField(max_length=30)
    shortname = models.CharField(max_length=15)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name
