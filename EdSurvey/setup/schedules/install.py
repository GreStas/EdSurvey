from datetime import timedelta

from django.utils.timezone import now

from ..querylists import install
from ..querylists.install import querylist1, querylist2, querylist3
from ..clients.install import \
    division_the_site, site1_user, \
    division_sbrf, sbrf1_user, sbrf2_user, sbrf1_schedule_manager, squad_sbrf_users, \
    division_freebee, freebee_user, freebee_superuser, squad_freebee_users, squad_freebee_all

from schedules.models import Task, Schedule


def add_schedule(task, start, finish, name, description, owner, squads):
    print("Adding schedule: task={}, name={} ".format(task, name))
    print("         squads:", ", ".join(('"{}"'.format(r) for r in squads)))
    schedule = Schedule(
        task=task,
        start=start,
        finish=finish,
        name=name,
        description=description,
        owner=owner,
    )
    schedule.save()
    schedule.squads.add(*squads)
    return schedule

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
task1_sched1 = add_schedule(
    task=task1,
    start=now(),
    finish=now() + timedelta(hours=1),
    name="на 1 час",
    description="""доступен в течении 1 часа""",
    owner=site1_user,
    squads=(squad_freebee_users, squad_sbrf_users,),
)
task1_sched2 = add_schedule(
    task=task1,
    start=now(),
    finish=now() + timedelta(days=1),
    name="на 1 день",
    description="""доступен в течении суток""",
    owner=site1_user,
    squads=(squad_freebee_users, squad_sbrf_users,),
)
# task1_sched3 = add_schedule(
#     task=task1,
#     start=now(),
#     finish=now() + timedelta(days=1),
#     name="до конца дня",
#     description="""доступен до полуночи""",
# )
task1_sched4 = add_schedule(
    task=task1,
    start=now(),
    finish=now() + timedelta(days=31),
    name="на 1 месяц",
    description="""доступен в течении месяца""",
    owner=site1_user,
    squads=(squad_freebee_users, squad_sbrf_users,),
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
task2_sched1 = add_schedule(
    task=task2,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
    owner=sbrf1_user,
    squads=(squad_sbrf_users,),
)

task3 = Task.objects.create(
    querylist=querylist2,
    attempts=999,
    viewable=True,
    editable=True,
    autoclose=False,
    description="""Для отладки Editable Viewable not Autoclose""",
    name="Edit View NoAuto",
    division=division_the_site,
    public=True,
    owner=sbrf1_schedule_manager,
)
task3_sched1 = add_schedule(
    task=task3,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
    owner=sbrf1_schedule_manager,
    squads=(squad_freebee_users, squad_sbrf_users,),
)

task4 = Task.objects.create(
    querylist=querylist2,
    attempts=999,
    viewable=False,
    editable=True,
    autoclose=False,
    description="""Для отладки Editable not Viewable Autoclose""",
    name="Edit noView NoAuto",
    division=division_the_site,
    public=True,
    owner=sbrf1_schedule_manager,
)
task4_sched1 = add_schedule(
    task=task4,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
    owner=sbrf1_user,
    squads=(squad_freebee_users, squad_sbrf_users,),
)

task5 = Task.objects.create(
    querylist=querylist2,
    attempts=999,
    viewable=True,
    editable=False,
    autoclose=False,
    description="""Для отладки not Editable Viewable not Autoclose""",
    name="NoEdit View NoAuto",
    division=division_the_site,
    public=True,
    owner=sbrf1_schedule_manager,
)
task5_sched1 = add_schedule(
    task=task5,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
    owner=sbrf1_schedule_manager,
    squads=(squad_freebee_users, squad_sbrf_users,),
)

task6 = Task.objects.create(
    querylist=querylist2,
    attempts=999,
    viewable=False,
    editable=False,
    autoclose=False,
    description="""Для отладки not Editable not Viewable not Autoclose""",
    name="NoEdit NoView NoAuto",
    division=division_freebee,
    public=True,
    owner=freebee_user,
)
task6_sched1 = add_schedule(
    task=task6,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
    owner=freebee_user,
    squads=(squad_freebee_users,),
)

task7 = Task.objects.create(
    querylist=querylist2,
    attempts=999,
    viewable=False,
    editable=False,
    autoclose=True,
    description="""Для отладки not Editable not Viewable Autoclose""",
    name="NoEdit NoView Auto",
    division=division_the_site,
    public=True,
    owner=freebee_superuser,
)
task7_sched1 = add_schedule(
    task=task7,
    start=now(),
    finish=now() + timedelta(days=31),
    name="для отладки",
    description="""доступен в течении месяца""",
    owner=freebee_user,
    squads=(squad_freebee_users, squad_sbrf_users,),
)
