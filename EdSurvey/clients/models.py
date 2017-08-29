from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models.signals import post_save, pre_save

from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.utils.timezone import now


class Client(models.Model):
    name = models.CharField('название', max_length=60)
    shortname = models.CharField('абревиатура', max_length=30)
    corporate = models.BooleanField('корпорация', default=False)
    public = models.BooleanField('публичный контент', default=True)

    def delete(self, *args, **kwargs):
        if self.id == 1:
            raise ValidationError("Нельзя удалить Корневого Клиента.")
        super(Client, self).delete(*args, **kwargs)

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

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
    name = models.CharField('название', max_length=60)
    shortname = models.CharField('абревиатура', max_length=15)
    public = models.BooleanField('публичный контент', default=False)
    private = models.BooleanField('контент только этого подразделения', default=False)

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
        verbose_name = 'организация'
        verbose_name_plural = 'организации'
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
        primary_key=True
        # parent_link=True,
    )
    fullname = models.CharField('полное наименование', max_length=120)
    address = models.TextField('почтовый адрес', null=True, blank=True)
    rootdivision = models.ForeignKey(Division,
                                     on_delete=models.PROTECT,
                                     verbose_name='корневая организация',)
    def save(self, **kwargs):
        # print(self.rootdivision.client.id, self.client_ptr.id)
        if self.rootdivision and self.rootdivision.client.id != self.client_ptr.id:
            raise ValidationError("Корневое подразделение указано не корректно.")
        super(ClientData, self).save(**kwargs)

    class Meta:
        verbose_name = 'дополнительная информация о Клиенте'
        verbose_name_plural = 'дополнительная информация о Клиентах'


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


class DataType(models.Model):
    name = models.CharField('название', max_length=60, unique=True)
    description = models.TextField('описание')
    applabel = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = (('applabel','model'),)

    def __str__(self):
        return "{}".format(self.name)


class Role(models.Model):
    """ Role
    name
    shortname
    description
    group(auth.group, default=allusers) - для фиксированных ролей типа Модератор Сайта, Администратор Сайта, Модератор, Редактор и другие (по мере создания). Должна быть фиксированная группа-Роль "Пользователи сайта", которая будет даваться по-молчанию.
    """
    name = models.CharField('название', max_length=60, unique=True)
    shortname = models.CharField('абревиатура', max_length=30, unique=True)
    description = models.TextField('описание')
    acls = models.ManyToManyField(DataType, through='RolePermission')

    class Meta:
        verbose_name = 'роль'
        verbose_name_plural = 'роли'

    def __str__(self):
        # return "{}{}".format(self.name, "/{}".format(self.group) if self.group else '')
        return "{}".format(self.name)


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    datatype = models.ForeignKey(DataType, on_delete=models.CASCADE)
    acl = models.CharField(max_length=10)

    class Meta:
        unique_together = (('role', 'datatype'),)

    def __str__(self):
        return "{} - {} - {}".format(self.role.shortname, self.datatype.name, self.acl)


# def has_permission(person, applabel, model, acl, exact=False):
#     """    Проверка на наличие запрошенных прав.
#     Если exact==True, то отсутвие любого права - это отсутсвие прав.
#     Если exact==False, то наличие хотя-бы одно права - это наличие прав.
#     :param person: Личность
#     :param applabel: Приложение
#     :param model: Модель
#     :param acl: Запрошенные для проверки права
#     :param exact: Полное наличие всех запрошенных прав?
#     :return: права из таблицы прав или None
#     """
#     try:
#         acls = RolePermission.objects.all().get(role=person.role, datatype__applabel=applabel, datatype__model=model).acl
#     except ObjectDoesNotExist:
#         return None
#     for r in acl:
#         if r in acls:
#             if not exact:
#                 # Если не требуется точное наличие всех запрошенных прав, то дальше можно и не проверять.
#                 break
#         elif exact:
#             # Если требуется точное наличие всех запрошенных прав и хотя-бо одно право не найдено,
#             # то дальше можно и не проверять и возвращаем None.
#             acls = None
#             break
#     return acls


class Person(models.Model):
    """ Личность
    Позволяет создать алисы пользователей сайта
    для дальнейшей работы с различными Клиентами
    """
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    shortname = models.CharField('aka', max_length=30)
    division = models.ForeignKey(Division, on_delete=models.PROTECT, verbose_name='входит в организацию')
    # role = models.ForeignKey(Role, on_delete=models.PROTECT, verbose_name='доступная роль')
    roles = models.ManyToManyField(Role, blank=True, verbose_name='роли')
    used = models.DateTimeField(auto_now_add=now())
    # clients = models.ManyToManyField(Client, verbose_name='от клиента')
    # divisions = models.ManyToManyField(Division, verbose_name='входит в организацию')
    # roles = models.ManyToManyField(Role, verbose_name='доступная роль')

    def get_permissions(self, datatype):
        """ Получить эффективные права на основе всех доступных ролей

        :param datatype:
        :return: string of rights
        """
        acls = set()
        for perm in RolePermission.objects.all().filter(datatype=datatype, role__in=self.roles.all()):
            acls = acls.union({r for r in perm.acl})
        return ''.join(acls)

    def get_perms(self, applabel, model):
        return self.get_permissions(DataType.objects.all().get(applabel=applabel, model=model))

    def has_permissions(self, datatype, acl):
        effective_acl = self.get_permissions(datatype)
        for i in acl:
            if i not in effective_acl:
                return False
        return True

    def has_perms(self, applabel, model, acl):
        return self.has_permissions(DataType.objects.all().get(applabel=applabel, model=model), acl)

    class Meta:
        verbose_name = 'личность'
        verbose_name_plural = 'личности'
        unique_together = (('user', 'shortname',),)

    def __str__(self):
        return '{} {} aka "{}"'.format(self.user.first_name, self.user.last_name, self.shortname)


def get_active_person(request):
    return get_object_or_404(Person, pk=request.session['person_id'])


class Squad(models.Model):
    """ Рабочая группа (бригада) """
    name = models.CharField('название', max_length=60)
    shortname = models.CharField('абревиатура', max_length=30)
    description = models.TextField('описание', null=True, blank=True)
    division = models.ForeignKey(Division, verbose_name='организация')
    # manager = models.ForeignKey(Person, blank=True, null=True, verbose_name='менеджер группы')
    members = models.ManyToManyField(Person, verbose_name='участники')

    class Meta:
        verbose_name = 'рабочая группа'
        verbose_name_plural = 'рабочие группы'
        unique_together = (('shortname', 'division',),)

    def __str__(self):
        return "{} для {}".format(self.shortname, self.division.shortname)


# class PersonCache(models.Model):
#     person_ptr = models.OneToOneField(
#         Person,
#         on_delete=models.CASCADE,
#         parent_link=True,
#     )
#     client = models.ForeignKey(Client, null=True)
#     division = models.ForeignKey(Division, null=True)
#     role = models.ForeignKey(Role, null=True)
#     used = models.DateTimeField(null=True)
