from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import models
from django.db.models import Q

from questions.models import Question
from clients.models import Division, Person, RolePermission

class QueryListManager(models.Manager):
    def perm(self, person, acl):
        qset = Q(owner=person) | Q(public=True)
        try:
            perms = RolePermission.objects.all().get(role=person.role,
                                                     datatype__applabel='querylists',
                                                     datatype__model='QueryList')
            for i in acl:
                if i in perms.acl:
                    qset |= Q(division=person.division)
                    break
        except ObjectDoesNotExist:
            pass
        return super().get_queryset().filter(qset)

    def get_queryset(self):
        res = super().get_queryset()
        return res


class QueryList(models.Model):
    name = models.CharField(max_length=60)
    description = models.TextField()
    division = models.ForeignKey(Division, on_delete=models.PROTECT)
    public = models.BooleanField(default=False)
    owner = models.ForeignKey(Person, on_delete=models.PROTECT, verbose_name='владелец')
    # status = models.IntegerField(null=True)
    # authors = models.ForeignKey('auth.User')
    # params xml

    objects = QueryListManager()

    class Meta:
        verbose_name = 'Опросник'
        verbose_name_plural = 'Опросники'

    def __str__(self):
        return "{}.{}".format(self.id, self.name)


class QueryContent(models.Model):
    querylist = models.ForeignKey(QueryList, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    ordernum = models.PositiveIntegerField(null=True, blank=True)
    # status = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Наполнение опросника'
        verbose_name_plural = 'Наполнение опросников'
        unique_together = ('querylist', 'question')

    def __str__(self):
        return "{}-{}".format(self.querylist, self.question)