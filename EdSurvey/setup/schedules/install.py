from datetime import timedelta

from django.utils.timezone import now

from ..querylists import install
from ..querylists.install import querylist1, querylist2, querylist3
from ..clients.install import division_the_site, division_sbrf

from schedules.models import Task, Schedule


task1 = Task.objects.create(
    querylist=querylist1,
    attempts=1,
    viewable=False,
    editable=False,
    autoclose=True,
    description="""NoEdit NoView Auto""",
    name="Для отладки расписаний",
    division=division_the_site,
    public=True,
)
task1_sched1 = Schedule.objects.create(
    task=task1,
    start=now(),
    finish=now() + timedelta(hours=1),
    name="на 1 час",
    description="""доступен в течении 1 часа""",
)
task1_sched2 = Schedule.objects.create(
    task=task1,
    start=now(),
    finish=now() + timedelta(days=1),
    name="на 1 день",
    description="""доступен в течении суток""",
)
# task1_sched3 = Schedule.objects.create(
#     task=task1,
#     start=now(),
#     finish=now() + timedelta(days=1),
#     name="до конца дня",
#     description="""доступен до полуночи""",
# )
task1_sched4 = Schedule.objects.create(
    task=task1,
    start=now(),
    finish=now() + timedelta(days=31),
    name="на 1 месяц",
    description="""доступен в течении месяца""",
)

task2 = Task.objects.create(
    querylist=querylist3,
    attempts=999,
    viewable=True,
    editable=True,
    autoclose=False,
    description="""Edit View NoAuto""",
    name="Для СБЕРБАНКА",
    division=division_sbrf,
    public=False,
)
task2_sched1 = Schedule.objects.create(
    task=task2,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
)

task3 = Task.objects.create(
    querylist=querylist2,
    attempts=999,
    viewable=True,
    editable=True,
    autoclose=False,
    description="""Для отладки Editable Viewable Autoclose""",
    name="Edit View NoAuto",
    division=division_the_site,
    public=True,
)
task3_sched1 = Schedule.objects.create(
    task=task3,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
)

task4 = Task.objects.create(
    querylist=querylist2,
    attempts=999,
    viewable=False,
    editable=True,
    autoclose=False,
    description="""Для отладки Editable Viewable Autoclose""",
    name="NoEdit View NoAuto",
    division=division_the_site,
    public=True,
)
task4_sched1 = Schedule.objects.create(
    task=task4,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
)

task5 = Task.objects.create(
    querylist=querylist2,
    attempts=999,
    viewable=True,
    editable=False,
    autoclose=False,
    description="""Для отладки Editable Viewable Autoclose""",
    name="Edit NoView NoAuto",
    division=division_the_site,
    public=True,
)
task5_sched1 = Schedule.objects.create(
    task=task5,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
)

task6 = Task.objects.create(
    querylist=querylist2,
    attempts=999,
    viewable=False,
    editable=False,
    autoclose=False,
    description="""Для отладки Editable Viewable Autoclose""",
    name="NoEdit NoView NoAuto",
    division=division_the_site,
    public=True,
)
task6_sched1 = Schedule.objects.create(
    task=task6,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
)

task7 = Task.objects.create(
    querylist=querylist2,
    attempts=999,
    viewable=False,
    editable=False,
    autoclose=True,
    description="""Для отладки Editable Viewable Autoclose""",
    name="NoEdit NoView Auto",
    division=division_the_site,
    public=True,
)
task7_sched1 = Schedule.objects.create(
    task=task7,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
)
