from django.db import models

class Answer(models.Model):
    question = models.ForeignKey('questions.Question')
    content = models.TextField()
    ordernum = models.PositiveIntegerField(null=True)
    score = models.PositiveIntegerField(null=True)
    # status = models.IntegerField(null=True)

