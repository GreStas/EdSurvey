from ..questions import install
from ..questions.install import site_q1, site_q2, site_q3, site_q4, site_q5
from ..clients.install import division_the_site, division_sbrf, site1_user, sbrf1_editor

from querylists.models import QueryList, QueryContent

querylist1 = QueryList.objects.create(
    name='Устройство котов',
    description="""Устройство котов напоминает устройство любого млекопитающего.
Однако есть некоторые отличия.
Эти отличия обусловлены тем, что кот одновременно является хищником и домашним животным.""",
    division=division_the_site,
    public=True,
    owner=site1_user,
)
querylist1_question1 = QueryContent.objects.create(
    querylist=querylist1,
    question=site_q1,
    ordernum=1,
)
querylist1_question2 = QueryContent.objects.create(
    querylist=querylist1,
    question=site_q2,
    ordernum=None,
)
querylist1_question3 = QueryContent.objects.create(
    querylist=querylist1,
    question=site_q3,
    ordernum=None,
)

querylist2 = QueryList.objects.create(
    name='Социализация котов',
    description="""Социальная жизнь котов разнообразна и отличается от жизни других животных.""",
    division=division_the_site,
    public=False,
    owner=site1_user,
)
querylist2_question1 = QueryContent.objects.create(
    querylist=querylist2,
    question=site_q4,
    ordernum=None,
)
querylist2_question2 = QueryContent.objects.create(
    querylist=querylist2,
    question=site_q5,
    ordernum=None,
)


querylist3 = QueryList.objects.create(
    name='Всё о котах',
    description="""Устройство котов напоминает устройство любого млекопитающего.
Однако есть некоторые отличия.
Эти отличия обусловлены тем, что кот одновременно является хищником и домашним животным.
Социальная жизнь котов разнообразна и отличается от жизни других животных.""",
    division=division_sbrf,
    public=True,
    owner=sbrf1_editor,
)
querylist3_question1 = QueryContent.objects.create(
    querylist=querylist3,
    question=site_q1,
    ordernum=None,
)
querylist3_question2 = QueryContent.objects.create(
    querylist=querylist3,
    question=site_q2,
    ordernum=None,
)
querylist3_question3 = QueryContent.objects.create(
    querylist=querylist3,
    question=site_q3,
    ordernum=None,
)
querylist3_question4 = QueryContent.objects.create(
    querylist=querylist3,
    question=site_q4,
    ordernum=None,
)
querylist3_question5 = QueryContent.objects.create(
    querylist=querylist3,
    question=site_q5,
    ordernum=None,
)
