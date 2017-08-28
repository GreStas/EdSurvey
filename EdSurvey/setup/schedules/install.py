from datetime import timedelta

from django.utils.timezone import now

from ..querylists import install
from ..querylists.install import querylist1, querylist2, querylist3
from ..clients.install import \
    division_the_site, site1_user, \
    division_sbrf, sbrf1_user, sbrf1_schedule_manager, \
    division_freebee, freebee_user, freebee_superuser

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
    owner=site1_user,
)
task1_sched1 = Schedule.objects.create(
    task=task1,
    start=now(),
    finish=now() + timedelta(hours=1),
    name="на 1 час",
    description="""доступен в течении 1 часа""",
    owner=site1_user,
)
task1_sched2 = Schedule.objects.create(
    task=task1,
    start=now(),
    finish=now() + timedelta(days=1),
    name="на 1 день",
    description="""доступен в течении суток""",
    owner=site1_user,
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
    owner=site1_user,
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
    owner=sbrf1_user,
)
task2_sched1 = Schedule.objects.create(
    task=task2,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
    owner=sbrf1_user,
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
    owner=sbrf1_schedule_manager,
)
task3_sched1 = Schedule.objects.create(
    task=task3,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
    owner=sbrf1_schedule_manager,
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
    owner=sbrf1_schedule_manager,
)
task4_sched1 = Schedule.objects.create(
    task=task4,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
    owner=sbrf1_user,
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
    owner=sbrf1_schedule_manager,
)
task5_sched1 = Schedule.objects.create(
    task=task5,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
    owner=sbrf1_schedule_manager,
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
    owner=freebee_user,
)
task6_sched1 = Schedule.objects.create(
    task=task6,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
    owner=freebee_user,
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
    owner=freebee_superuser,
)
task7_sched1 = Schedule.objects.create(
    task=task7,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
    owner=freebee_user,
)
