from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.db import models


class Question(models.Model):
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return "{}.{}.{}".format(self.id, self.qtype, self.description[:15])

    RADIOBUTTON = 'RB'  # (*) One -from- List
    CHECKBOX = 'CB'     # [v] Some -from- List
    LINKEDLISTS = 'LL'   # Link One from first list -to- One from other list
    QUESTION_TYPE_CHOICES = (
        (RADIOBUTTON, 'Один из ...'),
        (CHECKBOX, 'Несколько из ...'),
        (LINKEDLISTS, "Путанка"),
    )

    qtype = models.CharField(
        max_length=2,
        choices=QUESTION_TYPE_CHOICES,
        default=RADIOBUTTON,
    )
    description = models.TextField()
    # status = models.IntegerField(null=True)
    # content = models.XML - Как лучше хранить форматированный текст?
    # organisation = models.ForeignKey('organisations.organisation')
    # authors = models.ForeignKey('auth.User')

def question_pre_save(instance, **kwargs):
    # Проверка на изменение типа вопроса (qtype)
    # select 1 from Answer where Answer.question = self.id limit 1
    cntRB = AnswerRB.objects.all().filter(question=instance)[:1].count()
    cntCB = AnswerCB.objects.all().filter(question=instance)[:1].count()
    cntLL = AnswerLL.objects.all().filter(question=instance)[:1].count()
    print(instance.qtype, cntRB, cntCB, cntLL)
    if instance.qtype not in ('RB', 'CB', 'LL'):
        raise ValidationError(_("Unknown QType"))
    elif (instance.qtype == 'RB' and (cntCB + cntLL) > 0) or \
        (instance.qtype == 'CB' and (cntRB + cntLL) > 0) or \
        (instance.qtype == 'LL' and (cntRB + cntCB) > 0) :
        raise ValidationError("Нельзя изменять тип вопроса, если вопрос всё ещё имеет ответы.")

pre_save.connect(question_pre_save, sender=Question)


class Answer(models.Model):
    class Meta:
        verbose_name = 'Простой Ответ'
        verbose_name_plural = 'Простые Ответы'

    def __str__(self):
        return self.content

    question = models.ForeignKey('Question')
    content = models.TextField()
    ordernum = models.PositiveIntegerField(null=True, blank=True)
    score = models.PositiveIntegerField(null=True, blank=True)
    # status = models.IntegerField(null=True)


class AnswerRB(Answer):
    """ qtype == RB
        необходим для создания отдельных валидаторов
    """
    class Meta:
        verbose_name = 'Одиночный Ответ (RadioButton)'
        verbose_name_plural = 'Одиночные Ответы (RadioButton)'

    answer_ptr = models.OneToOneField(
        Answer, on_delete=models.CASCADE,
        parent_link=True,
    )

    def clean(self):
        qtype = self.question.qtype
        if qtype != 'RB':
            raise ValidationError("Тип вопроса ({}) и тип ответа (RB) не совпадают.".format(qtype))


class AnswerCB(Answer):
    """ qtype == CB
        необходим для создания отдельных валидаторов
    """
    class Meta:
        verbose_name = 'Множественный Ответ (CheckBox)'
        verbose_name_plural = 'Множественные Ответы (CheckBox)'

    answer_ptr = models.OneToOneField(
        Answer, on_delete=models.CASCADE,
        parent_link=True,
    )

    def clean(self):
        qtype = self.question.qtype
        if qtype != 'CB':
            raise ValidationError("Тип вопроса ({}) и тип ответа (CB) не совпадают.".format(qtype))


class AnswerLL(Answer):
    class Meta:
        verbose_name = 'Ответ-Путанка'
        verbose_name_plural = 'Ответы-Путанки'

    answer_ptr = models.OneToOneField(
        Answer, on_delete=models.CASCADE,
        parent_link=True,
    )
    linkeditem = models.TextField()
    ordernumitem = models.PositiveIntegerField(null=True, blank=True)

    def clean(self):
        qtype = self.question.qtype
        if qtype != 'LL':
            raise ValidationError("Тип вопроса ({}) и тип ответа (LL) не совпадают.".format(qtype))
