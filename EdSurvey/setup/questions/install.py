from ..clients import install

from ..clients.install import division_the_site, division_sbrf, site1_user, sbrf1_user, sbrf1_editor
from questions.models import Question, Answer, AnswerRB, AnswerCB, AnswerLL, RADIOBUTTON, CHECKBOX, LINKEDLISTS

site_q1 = Question.objects.create(
    name='хвосты и коты',
    description="""Наличие или отсутвие хвоста, а также его особенности - это важный признак для животного.
    А у котов есть хвост?""",
    division=division_the_site,
    public=True,
    qtype=RADIOBUTTON,
    owner=site1_user,
)
site_q1_answer1 = AnswerRB.objects.create(
    question=site_q1,
    content="""Нет""",
    ordernum=1,
    score=1,
    qtype=site_q1.qtype,
)
site_q1_answer2 = AnswerRB.objects.create(
    question=site_q1,
    content="""У некоторых""",
    ordernum=2,
    score=5,
    qtype=site_q1.qtype,
)
site_q1_answer3 = AnswerRB.objects.create(
    question=site_q1,
    content="""Да""",
    ordernum=3,
    score=10,
    qtype=site_q1.qtype,
)

site_q2 = Question.objects.create(
    name='из чего состоит кот',
    description="""Какие части тела есть у кота?""",
    division=division_the_site,
    public=True,
    qtype=CHECKBOX,
    owner=site1_user,
)
site_q2_answer1 = AnswerCB.objects.create(
    question=site_q2,
    content="""Шерсть""",
    ordernum=None,
    score=8,
    qtype=site_q2.qtype,
)
site_q2_answer2 = AnswerCB.objects.create(
    question=site_q2,
    content="""Клюв""",
    ordernum=None,
    score=1,
    qtype=site_q2.qtype,
)
site_q2_answer3 = AnswerCB.objects.create(
    question=site_q2,
    content="""Лапы""",
    ordernum=None,
    score=10,
    qtype=site_q2.qtype,
)

site_q3 = Question.objects.create(
    name='части тела кота',
    description="""Сопоставьте части тела кота и их количество:""",
    division=division_the_site,
    public=False,
    qtype=LINKEDLISTS,
    owner=sbrf1_editor,
)
site_q3_answer1 = AnswerLL.objects.create(
    question=site_q3,
    content="""Сколько у кота лап?""",
    ordernum=1,
    score=10,
    qtype=site_q3.qtype,
    linkeditem="""Четыре""",
    ordernumitem=None,
)
site_q3_answer2 = AnswerLL.objects.create(
    question=site_q3,
    content="""Сколько у кота хвостов?""",
    ordernum=None,
    score=10,
    qtype=site_q3.qtype,
    linkeditem="""Один / Одна""",
    ordernumitem=None,
)
site_q3_answer3 = AnswerLL.objects.create(
    question=site_q3,
    content="""Сколько у кота жизней?""",
    ordernum=None,
    score=10,
    qtype=site_q3.qtype,
    linkeditem="""Девять""",
    ordernumitem=None,
)
site_q3_answer4 = AnswerLL.objects.create(
    question=site_q3,
    content="""Сколько у кота ушей?""",
    ordernum=None,
    score=10,
    qtype=site_q3.qtype,
    linkeditem="""Два / Две""",
    ordernumitem=None,
)

site_q4 = Question.objects.create(
    name='что важно котам',
    description="""Перечислилте то, что главное для котов:""",
    division=division_the_site,
    public=True,
    qtype=CHECKBOX,
    owner=site1_user,
)
site_q4_answer1 = AnswerCB.objects.create(
    question=site_q4,
    content="""Хозяин""",
    ordernum=None,
    score=5,
    qtype=site_q4.qtype,
)
site_q4_answer2 = AnswerCB.objects.create(
    question=site_q4,
    content="""Дом""",
    ordernum=None,
    score=10,
    qtype=site_q4.qtype,
)
site_q4_answer3 = AnswerCB.objects.create(
    question=site_q4,
    content="""Место""",
    ordernum=None,
    score=9,
    qtype=site_q4.qtype,
)
site_q4_answer4 = AnswerCB.objects.create(
    question=site_q4,
    content="""Человек""",
    ordernum=None,
    score=3,
    qtype=site_q4.qtype,
)

site_q5 = Question.objects.create(
    name='коты и другие животные',
    description="""Как коты относятся к другим животным? Сопоставьте вопросы и ответы:""",
    division=division_the_site,
    public=True,
    qtype=LINKEDLISTS,
    owner=site1_user,
)
site_q5_answer1 = AnswerLL.objects.create(
    question=site_q5,
    content="""Коты дружат с ...""",
    ordernum=None,
    score=10,
    qtype=site_q5.qtype,
    linkeditem="""кошками""",
    ordernumitem=None,
)
site_q5_answer2 = AnswerLL.objects.create(
    question=site_q5,
    content="""Коты враждуют с ...""",
    ordernum=None,
    score=10,
    qtype=site_q5.qtype,
    linkeditem="""собаками""",
    ordernumitem=None,
)
site_q5_answer3 = AnswerLL.objects.create(
    question=site_q5,
    content="""Коты дерутся с ...""",
    ordernum=None,
    score=10,
    qtype=site_q5.qtype,
    linkeditem="""котами""",
    ordernumitem=None,
)
site_q5_answer4 = AnswerLL.objects.create(
    question=site_q5,
    content="""Коты ловят ...""",
    ordernum=None,
    score=10,
    qtype=site_q5.qtype,
    linkeditem="""птиц""",
    ordernumitem=None,
)
site_q5_answer5 = AnswerLL.objects.create(
    question=site_q5,
    content="""Коты любят есть ...""",
    ordernum=None,
    score=10,
    qtype=site_q5.qtype,
    linkeditem="""рыбу""",
    ordernumitem=None,
)
site_q5_answer6 = AnswerLL.objects.create(
    question=site_q5,
    content="""Коты любят пить ...""",
    ordernum=None,
    score=10,
    qtype=site_q5.qtype,
    linkeditem="""молоко""",
    ordernumitem=None,
)
