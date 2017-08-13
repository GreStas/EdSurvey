from django.core.exceptions import ValidationError
from django.db import models


# ROOT_OWNER_NAME = 'Владелец сайта'
# ROOT_OWNER_SHORTNAME = 'THE_OWNER'
# ROOT_DIVISION_NAME = 'Опросы и Тестирование'
# ROOT_DIVISION_SHORTNAME = 'THE_SITE'


class Client(models.Model):
    name = models.CharField(max_length=30)
    shortname = models.CharField(max_length=15)

    def delete(self, *args, **kwargs):
        if self.id == 1:
            raise ValidationError("Нельзя удалить Корневого Клиента.")
        super(Client, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.name



class Division(models.Model):
    """
    public - определяет, что весь контент этой организации будет доступен всем организациями и пользователям сайта.
    private - определяет, что это корпорация и у неё будет свой штат управления.
    public==False and private==False - означает, что для каждого созданного пользователем теста необходимо создать уникальную группу доступа.
    public==True and private==True - означает, что Организация делится своим контентом и имеет свою систему управления.
    id==1 - {'public':False, 'private':False, 'client':1} - superorganisation for superclient.
    """
    client = models.ForeignKey(Client, on_delete=models.PROTECT)
    name = models.CharField(max_length=60)
    shortname = models.CharField(max_length=15)
    public = models.BooleanField(default=False)
    private = models.BooleanField(default=False)

    def delete(self, *args, **kwargs):
        if self.id == 1:
            raise ValidationError("Нельзя удалить Корневую оргструктуру.")
        super(Division, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'
        unique_together = (
            ('client', 'shortname'),
            ('client', 'name'),
        )

    def __str__(self):
        return self.name
