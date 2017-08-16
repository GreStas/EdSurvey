from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save, pre_save


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
            raise ValidationError("Нельзя удалить Корневую оргструктуру Сайта.")
        if self.client.division_id == self.id:
            raise ValidationError("Нельзя удалить Корневую оргструктуру Клиента.")
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
    address = models.TextField('почтовый адрес')
    rootdivision = models.ForeignKey(Division,
                                     on_delete=models.CASCADE,
                                     verbose_name='корневая организация',)

    class Meta:
        verbose_name = 'Дополнительная информация о Клиенте'
        verbose_name_plural = 'Дополнительная информация о Клиентах'


# # def client_pre_save(instance, **kwargs):
# #     """ Очистить division_id, если организация не корректна"""
# #     if instance.division_id:
# #         try:
# #             division = Division.objects.get(id=instance.division_id,
# #                                             client=instance)
# #         except ObjectDoesNotExist:
# #             ValueError("Корневое подразделение указано не корректно.")
# #
# # pre_save.connect(client_pre_save, sender=Client)
# #
# #
# # def client_post_save(instance, **kwargs):
# #     """
# #     Ищем организацию с совпадающими name и shortname
# #     Если таковая не находится, то создаём её.
# #     """
# #     if instance.division_id:
# #         try:
# #             division = Division.objects.get(id=instance.division_id,
# #                                             client=instance)
# #         except ObjectDoesNotExist:
# #             ValidationError("Корневое подразделение указано не корректно.")
# #     else:
# #         try:
# #             division = Division.objects.get(client=instance,
# #                                             name=instance.name,
# #                                             shortname=instance.shortname)
# #         except ObjectDoesNotExist:
# #             division = Division.objects.create(client=instance,
# #                                                name=instance.name,
# #                                                shortname=instance.shortname,
# #                                                )
# #             # division.save()
# #
# # post_save.connect(client_post_save, sender=Client)
