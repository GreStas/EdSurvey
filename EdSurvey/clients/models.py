from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save, pre_save

from django.contrib.auth.models import User


class Client(models.Model):
    name = models.CharField('Название', max_length=30)
    shortname = models.CharField('Аббревиатура', max_length=15)
    corporate = models.BooleanField('Корпорация', default=False)
    public = models.BooleanField('Публичный контент', default=True)

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
    name = models.CharField('Название', max_length=60)
    shortname = models.CharField('Аббревиатура', max_length=15)
    public = models.BooleanField('Публичный контент', default=False)
    private = models.BooleanField('Контент только этого подразделения', default=False)

    def delete(self, *args, **kwargs):
        if self.id == 1:
            raise ValidationError("Нельзя удалить Корневую организацию Сайта.")
        try:
            clientdata = ClientData.objects.get(client_ptr=self.client)
            if clientdata.rootdivision == self:
                raise ValidationError("Нельзя удалить Корневую организацию Клиента.")
        except ObjectDoesNotExist:
            # Если нет доп.данных, то и проблемы нет.
            pass
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


class ClientData(models.Model):
    client_ptr = models.OneToOneField(
        Client,
        on_delete=models.CASCADE,
        parent_link=True,
    )
    fullname = models.CharField('полное наименование', max_length=120)
    address = models.TextField('почтовый адрес', null=True, blank=True)
    rootdivision = models.ForeignKey(Division,
                                     on_delete=models.CASCADE,
                                     verbose_name='корневая организация',)
    def save(self, **kwargs):
        # print(self.rootdivision.client.id, self.client_ptr.id)
        if self.rootdivision and self.rootdivision.client.id != self.client_ptr.id:
            raise ValidationError("Корневое подразделение указано не корректно.")
        super(ClientData, self).save(**kwargs)

    class Meta:
        verbose_name = 'Дополнительная информация о Клиенте'
        verbose_name_plural = 'Дополнительная информация о Клиентах'


def division_post_save(instance, **kwargs):
    """
    Если это первая организация Клиента,
    то автосоздание и автозаполнение доп.данных Клиента.
    """
    # cnt = Division.objects.all().filter(client=instance.client).count()
    # print(cnt)
    if Division.objects.all().filter(client=instance.client).count() <= 1:
        try:
            clientdata = ClientData.objects.get(client_ptr=instance.client)
        except ObjectDoesNotExist:
            ClientData.objects.create(client_ptr=instance.client,
                                      fullname=instance.client.name,
                                      rootdivision=instance)

post_save.connect(division_post_save, sender=Division)


class Person(models.Model):
    """ Личность
    Позволяет создать алисы пользователей сайта
    для дальнейшей работы с различными Клиентами
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    shortname = models.CharField(max_length=15)


    class Meta:
        verbose_name = 'Личность'
        verbose_name_plural = 'Личности'

    def __str__(self):
        return '{} {} aka "{}"'.format(self.user.first_name, self.user.last_name, self.shortname)

# class Squad(models.Model):
#     """ Рабочая группа (бригада) """
#     name = models.CharField('название', max_length=30)
#     shortname = models.CharField('абревиатура', max_length=15)
#     discription = models.TextField('описание', null=True, blank=True)
#     division = models.ForeignKey(Division, )  # TODO добавить default=корневая()
#     manager = models.ForeignKey(Person)
