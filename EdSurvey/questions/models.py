from django.db import models


class QType(models.Model):
    name = models.CharField(max_length=16)
    # status = models.IntegerField(null=True)


class Question(models.Model):
    qtype = models.ForeignKey('QType')
    description = models.TextField()
    # status = models.IntegerField(null=True)
    # content = models.XML
    # organisation = models.ForeignKey('organisations.organisation')
    # authors = models.ForeignKey('auth.User')
