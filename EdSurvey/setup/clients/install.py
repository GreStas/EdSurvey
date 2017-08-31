from ..home import install


#
#   clients Client
#
from clients.models import Client

client_the_site = Client.objects.create(
    id=1,
    name='Опросы и Тестирование',
    shortname='THE SITE',
    corporate=True,
    public=True,
)
client_sbrf = Client.objects.create(
    name='СБЕРБАНК',
    shortname='SBRF',
    corporate=True,
    public=False,
)
client_freebee = Client.objects.create(
    name='Халява',
    shortname='FREEBEE',
    corporate=False,
    public=True,
)


#
#   clients Division
#
from clients.models import Division

division_the_site = Division.objects.create(
    id=1,
    client=client_the_site,
    name=client_the_site.name,
    shortname=client_the_site.shortname,
    public=False,
    private=False,
)
division_the_site_common = Division.objects.create(
    client=client_the_site,
    name='Общедоступные опросы',
    shortname='COMMON',
    public=True,
    private=False,
)

division_sbrf = Division.objects.create(
    client=client_sbrf,
    name=client_sbrf.name,
    shortname=client_sbrf.shortname,
    public=False,
    private=False,
)
division_sbrf_urikit = Division.objects.create(
    client=client_sbrf,
    name='Управление развития и контроля',
    shortname='УРиКИТ',
    public=False,
    private=True,
)
division_sbrf_hr = Division.objects.create(
    client=client_sbrf,
    name='Управление персоналом',
    shortname='HR',
    public=True,
    private=True,
)
division_sbrf_staff = Division.objects.create(
    client=client_sbrf,
    name='Сотрудники',
    shortname='STAFF',
    public=True,
    private=False,
)

division_freebee = Division.objects.create(
    client=client_freebee,
    name=client_freebee.name,
    shortname=client_freebee.shortname,
    public=True,
    private=False,
)

#
#   clients ClientData
#
from clients.models import ClientData

client_the_site_data = ClientData(
    client_ptr=client_the_site,
    fullname='Сайт опросов и тестирования',
    address="""Украина, Киев, Героев Днепра, 38-е, 119""",
    rootdivision=division_the_site,
)
client_the_site_data.save()

client_sbrf_data = ClientData(
    client_ptr=client_sbrf,
    fullname='ПАО "СБЕРБАНК"',
    address="""Украина, Киев, Владимирская, 46""",
    rootdivision = division_sbrf,
)
client_sbrf_data.save()

client_freebee_data = ClientData(
    client_ptr=client_freebee,
    fullname='Сообщество халявщиков',
    address="""СССР""",
    rootdivision=division_freebee,
)
client_freebee_data.save()


#
#   clients DataType
#
from clients.models import DataType

questions_question = DataType.objects.create(
    name='Вопрос',
    description="""Формулировка и свойства вопроса""",
    applabel='questions',
    model='Question',
)
questions_answer = DataType.objects.create(
    name='Ответ',
    description="""Формулировка и свойства ответа""",
    applabel='questions',
    model='Answer',
)

querylists_querylist = DataType.objects.create(
        name='Опросный лист',
        description="""Опросный лист""",
        applabel='querylists',
        model='QueryList',
    )
querylists_querycontent = DataType.objects.create(
    name='Список вопросов',
    description="""Вопросы в опросном листе""",
    applabel='querylists',
    model='QueryContent',
)

schedules_task = DataType.objects.create(
    name='Задание',
    description="""Формулировка и свойства задания на тестирвоание""",
    applabel='schedules',
    model='Task',
)
schedules_schedule = DataType.objects.create(
    name='Расписание',
    description="""Расписание - временные параметры для Задания""",
    applabel='schedules',
    model='Schedule',
)
schedules_attempt = DataType.objects.create(
    name='Попытка',
    description="""Поптыка пройти задание""",
    applabel='schedules',
    model='Attempt',
)

surveys_anketa = DataType.objects.create(
    name='Анкета',
    description="""Сгенерированный на основе Опросника Задания список вопросов""",
    applabel='surveys',
    model='Anketa',
)
surveys_result = DataType.objects.create(
    name='Результат',
    description="""результат - это ответ, данный на пункт Анкеты""",
    applabel='surveys',
    model='Result',
)
clients_client = DataType.objects.create(
    name='Клиент',
    description="""Базовые параметры Клиента""",
    applabel='clients',
    model='Client',
)
clients_clientdata = DataType.objects.create(
    name='доп.данные Клиента',
    description="""Дополнительные параметры Клиента""",
    applabel='clients',
    model='ClientData',
)
clients_division = DataType.objects.create(
    name='Организация',
    description="""Огранизация или подразделение Клиента с признаком Корпорация""",
    applabel='clients',
    model='Division',
)
clients_role = DataType.objects.create(
    name='Роль',
    description="""Роль""",
    applabel='clients',
    model='Role',
)
clients_person = DataType.objects.create(
    name='Личность',
    description="""Личность определяет Роль Пользователя в Организации""",
    applabel='clients',
    model='Person',
)
clients_squad = DataType.objects.create(
    name='Бригада',
    description="""Бригада - это рабочая группа, которую можно использовать для наделения правами:
    - прохождения теста
    - (в будущем) авторства экземпляров модели - аналога owner""",
    applabel='clients',
    model='Squad',
)
"""
 = DataType.objects.create(
    name='',
    description="""""",
    applabel='',
    model='',
)
"""


#
#   clients Role
#
from clients.models import Role

role_user = Role.objects.create(
    id=0,
    name='Пользователь',
    shortname='USER',
    description="""Предопределённая Роль - могут создавать свой персональный контент и использовать публичный.""",
)
role_testee = Role.objects.create(
    id=1,
    name='Тестируемый',
    shortname='TESTEE',
    description="""Предопределённая Роль - могут проходить назначенные и публичные опросы.""",
)
role_editor = Role.objects.create(
    name='Редактор',
    shortname='EDITOR',
    description="""Создаёт и изменяет контент""",
)
role_content_manager = Role.objects.create(
    name='Менеджер контента',
    shortname='CONTENT_MGR',
    description="""Управляет правами на контент""",
)
role_schedule_manager = Role.objects.create(
    name='Менеджер заданий',
    shortname='SCHEDULE_MGR',
    description="""Управляет заданиями и расписаниями по ним""",
)
role_account_manager = Role.objects.create(
    name='Менеджер',
    shortname='ACCOUNT_MGR',
    description="""Управляет персоналом клиента""",
)
role_client_manager = Role.objects.create(
    name='Менеджер клиента',
    shortname='CLIENT_MGR',
    description="""Управляет объектами клиента""",
)
role_moderator = Role.objects.create(
    name='Модератор',
    shortname='MODERATOR',
    description="""Видит всё, кроме ответов и управлет оргструктурой клиента""",
)
role_analyst = Role.objects.create(
    name='Аналитик',
    shortname='ANALYST',
    description="""Формирует аналитику и статистику""",
)
role_administrator = Role.objects.create(
    name='Администратор',
    shortname='ADMINISTRATOR',
    description="""Управляет правами на права на объекты""",
)


#
#   clients RolePermision
#
from clients.models import RolePermission
"""
RolePermission.objects.create(role=role_, datatype=s_, acl='LRCUDM')
"""
RolePermission.objects.create(role=role_user, datatype=questions_answer, acl='O')
RolePermission.objects.create(role=role_user, datatype=questions_question, acl='O')
RolePermission.objects.create(role=role_user, datatype=querylists_querylist, acl='O')
RolePermission.objects.create(role=role_user, datatype=querylists_querycontent, acl='O')
RolePermission.objects.create(role=role_user, datatype=schedules_task, acl='O')
RolePermission.objects.create(role=role_user, datatype=schedules_schedule, acl='O')
RolePermission.objects.create(role=role_user, datatype=schedules_attempt, acl='O')
RolePermission.objects.create(role=role_user, datatype=surveys_anketa, acl='O')
RolePermission.objects.create(role=role_user, datatype=surveys_result, acl='O')
# RolePermission.objects.create(role=role_siteuser, datatype=clients_client, acl='O')
# RolePermission.objects.create(role=role_siteuser, datatype=clients_clientdata, acl='O')
# RolePermission.objects.create(role=role_siteuser, datatype=clients_division, acl='O')
RolePermission.objects.create(role=role_user, datatype=clients_role, acl='O')
RolePermission.objects.create(role=role_user, datatype=clients_person, acl='O')
RolePermission.objects.create(role=role_user, datatype=clients_squad, acl='O')

RolePermission.objects.create(role=role_testee, datatype=questions_answer, acl='T')
RolePermission.objects.create(role=role_testee, datatype=questions_question, acl='T')
RolePermission.objects.create(role=role_testee, datatype=querylists_querylist, acl='T')
RolePermission.objects.create(role=role_testee, datatype=querylists_querycontent, acl='T')
RolePermission.objects.create(role=role_testee, datatype=schedules_task, acl='T')
RolePermission.objects.create(role=role_testee, datatype=schedules_schedule, acl='T')
RolePermission.objects.create(role=role_testee, datatype=schedules_attempt, acl='T')
RolePermission.objects.create(role=role_testee, datatype=surveys_anketa, acl='T')
RolePermission.objects.create(role=role_testee, datatype=surveys_result, acl='T')
RolePermission.objects.create(role=role_testee, datatype=clients_client, acl='T')
RolePermission.objects.create(role=role_testee, datatype=clients_clientdata, acl='T')
RolePermission.objects.create(role=role_testee, datatype=clients_division, acl='T')
RolePermission.objects.create(role=role_testee, datatype=clients_role, acl='T')
RolePermission.objects.create(role=role_testee, datatype=clients_person, acl='T')
RolePermission.objects.create(role=role_testee, datatype=clients_squad, acl='T')

RolePermission.objects.create(role=role_editor, datatype=questions_answer, acl='LRCUD')
RolePermission.objects.create(role=role_editor, datatype=questions_question, acl='LRCUD')
RolePermission.objects.create(role=role_editor, datatype=querylists_querylist, acl='LRCUD')
RolePermission.objects.create(role=role_editor, datatype=querylists_querycontent, acl='LRCUD')
# RolePermission.objects.create(role=role_editor, datatype=schedules_task, acl='LRCUDM')
# RolePermission.objects.create(role=role_editor, datatype=schedules_schedule, acl='LRCUDM')
# RolePermission.objects.create(role=role_editor, datatype=schedules_attempt, acl='LRCUDM')
# RolePermission.objects.create(role=role_editor, datatype=surveys_anketa, acl='LRCUDM')
# RolePermission.objects.create(role=role_editor, datatype=surveys_result, acl='LRCUDM')
# RolePermission.objects.create(role=role_editor, datatype=clients_client, acl='LRCUDM')
# RolePermission.objects.create(role=role_editor, datatype=clients_clientdata, acl='LRCUDM')
# RolePermission.objects.create(role=role_editor, datatype=clients_division, acl='LRCUDM')
# RolePermission.objects.create(role=role_editor, datatype=clients_role, acl='LRCUDM')
# RolePermission.objects.create(role=role_editor, datatype=clients_person, acl='LRCUDM')
# RolePermission.objects.create(role=role_editor, datatype=clients_squad, acl='LRCUDM')

RolePermission.objects.create(role=role_content_manager, datatype=questions_answer, acl='M')
RolePermission.objects.create(role=role_content_manager, datatype=questions_question, acl='M')
RolePermission.objects.create(role=role_content_manager, datatype=querylists_querylist, acl='M')
RolePermission.objects.create(role=role_content_manager, datatype=querylists_querycontent, acl='M')
RolePermission.objects.create(role=role_content_manager, datatype=schedules_task, acl='R')
RolePermission.objects.create(role=role_content_manager, datatype=schedules_schedule, acl='R')
RolePermission.objects.create(role=role_content_manager, datatype=schedules_attempt, acl='L')
RolePermission.objects.create(role=role_content_manager, datatype=surveys_anketa, acl='L')
# RolePermission.objects.create(role=role_content_manager, datatype=surveys_result, acl='LRCUDM')
# RolePermission.objects.create(role=role_content_manager, datatype=clients_client, acl='LRCUDM')
# RolePermission.objects.create(role=role_content_manager, datatype=clients_clientdata, acl='LRCUDM')
# RolePermission.objects.create(role=role_content_manager, datatype=clients_division, acl='LRCUDM')
# RolePermission.objects.create(role=role_content_manager, datatype=clients_role, acl='LRCUDM')
# RolePermission.objects.create(role=role_content_manager, datatype=clients_person, acl='LRCUDM')
# RolePermission.objects.create(role=role_content_manager, datatype=clients_squad, acl='LRCUDM')

# RolePermission.objects.create(role=role_schedule_manager, datatype=questions_answer, acl='LRCUDM')
# RolePermission.objects.create(role=role_schedule_manager, datatype=questions_question, acl='LRCUDM')
RolePermission.objects.create(role=role_schedule_manager, datatype=querylists_querylist, acl='L')
# RolePermission.objects.create(role=role_schedule_manager, datatype=querylists_querycontent, acl='LRCUDM')
RolePermission.objects.create(role=role_schedule_manager, datatype=schedules_task, acl='LRCUD')
RolePermission.objects.create(role=role_schedule_manager, datatype=schedules_schedule, acl='LRCUD')
RolePermission.objects.create(role=role_schedule_manager, datatype=schedules_attempt, acl='L')
RolePermission.objects.create(role=role_schedule_manager, datatype=surveys_anketa, acl='L')
# RolePermission.objects.create(role=role_schedule_manager, datatype=surveys_result, acl='LRCUDM')
RolePermission.objects.create(role=role_schedule_manager, datatype=clients_client, acl='L')
# RolePermission.objects.create(role=role_schedule_manager, datatype=clients_clientdata, acl='LRCUDM')
RolePermission.objects.create(role=role_schedule_manager, datatype=clients_division, acl='L')
# RolePermission.objects.create(role=role_schedule_manager, datatype=clients_role, acl='LRCUDM')
# RolePermission.objects.create(role=role_schedule_manager, datatype=clients_person, acl='LRCUDM')
RolePermission.objects.create(role=role_schedule_manager, datatype=clients_squad, acl='L')

# RolePermission.objects.create(role=role_account_manager, datatype=questions_answer, acl='LRCUDM')
# RolePermission.objects.create(role=role_account_manager, datatype=questions_question, acl='LRCUDM')
# RolePermission.objects.create(role=role_account_manager, datatype=querylists_querylist, acl='LRCUDM')
# RolePermission.objects.create(role=role_account_manager, datatype=querylists_querycontent, acl='LRCUDM')
RolePermission.objects.create(role=role_account_manager, datatype=schedules_task, acl='R')
RolePermission.objects.create(role=role_account_manager, datatype=schedules_schedule, acl='R')
RolePermission.objects.create(role=role_account_manager, datatype=schedules_attempt, acl='R')
# RolePermission.objects.create(role=role_account_manager, datatype=surveys_anketa, acl='LRCUDM')
# RolePermission.objects.create(role=role_account_manager, datatype=surveys_result, acl='LRCUDM')
RolePermission.objects.create(role=role_account_manager, datatype=clients_client, acl='L')
RolePermission.objects.create(role=role_account_manager, datatype=clients_clientdata, acl='L')
RolePermission.objects.create(role=role_account_manager, datatype=clients_division, acl='L')
RolePermission.objects.create(role=role_account_manager, datatype=clients_role, acl='L')
RolePermission.objects.create(role=role_account_manager, datatype=clients_person, acl='LRCUD')
RolePermission.objects.create(role=role_account_manager, datatype=clients_squad, acl='LRCUD')

# RolePermission.objects.create(role=role_client_manager, datatype=questions_answer, acl='LRCUDM')
# RolePermission.objects.create(role=role_client_manager, datatype=questions_question, acl='LRCUDM')
# RolePermission.objects.create(role=role_client_manager, datatype=querylists_querylist, acl='LRCUDM')
# RolePermission.objects.create(role=role_client_manager, datatype=querylists_querycontent, acl='LRCUDM')
RolePermission.objects.create(role=role_client_manager, datatype=schedules_task, acl='L')
RolePermission.objects.create(role=role_client_manager, datatype=schedules_schedule, acl='L')
# RolePermission.objects.create(role=role_client_manager, datatype=schedules_attempt, acl='LRCUDM')
# RolePermission.objects.create(role=role_client_manager, datatype=surveys_anketa, acl='LRCUDM')
# RolePermission.objects.create(role=role_client_manager, datatype=surveys_result, acl='LRCUDM')
RolePermission.objects.create(role=role_client_manager, datatype=clients_client, acl='R')
RolePermission.objects.create(role=role_client_manager, datatype=clients_clientdata, acl='R')
RolePermission.objects.create(role=role_client_manager, datatype=clients_division, acl='LRCUD')
RolePermission.objects.create(role=role_client_manager, datatype=clients_role, acl='R')
RolePermission.objects.create(role=role_client_manager, datatype=clients_person, acl='M')
RolePermission.objects.create(role=role_client_manager, datatype=clients_squad, acl='M')

# RolePermission.objects.create(role=role_moderator, datatype=questions_answer, acl='LRCUDM')
RolePermission.objects.create(role=role_moderator, datatype=questions_question, acl='L')
RolePermission.objects.create(role=role_moderator, datatype=querylists_querylist, acl='L')
RolePermission.objects.create(role=role_moderator, datatype=querylists_querycontent, acl='L')
RolePermission.objects.create(role=role_moderator, datatype=schedules_task, acl='L')
RolePermission.objects.create(role=role_moderator, datatype=schedules_schedule, acl='L')
RolePermission.objects.create(role=role_moderator, datatype=schedules_attempt, acl='L')
RolePermission.objects.create(role=role_moderator, datatype=surveys_anketa, acl='L')
# RolePermission.objects.create(role=role_moderator, datatype=surveys_result, acl='LRCUDM')
RolePermission.objects.create(role=role_moderator, datatype=clients_client, acl='R')
RolePermission.objects.create(role=role_moderator, datatype=clients_clientdata, acl='LRCUD')
RolePermission.objects.create(role=role_moderator, datatype=clients_division, acl='LRCUD')
RolePermission.objects.create(role=role_moderator, datatype=clients_role, acl='R')
# RolePermission.objects.create(role=role_moderator, datatype=clients_person, acl='LRCUDM')
# RolePermission.objects.create(role=role_moderator, datatype=clients_squad, acl='LRCUDM')

RolePermission.objects.create(role=role_analyst, datatype=questions_answer, acl='R')
RolePermission.objects.create(role=role_analyst, datatype=questions_question, acl='R')
RolePermission.objects.create(role=role_analyst, datatype=querylists_querylist, acl='R')
RolePermission.objects.create(role=role_analyst, datatype=querylists_querycontent, acl='R')
RolePermission.objects.create(role=role_analyst, datatype=schedules_task, acl='R')
RolePermission.objects.create(role=role_analyst, datatype=schedules_schedule, acl='R')
RolePermission.objects.create(role=role_analyst, datatype=schedules_attempt, acl='R')
RolePermission.objects.create(role=role_analyst, datatype=surveys_anketa, acl='R')
RolePermission.objects.create(role=role_analyst, datatype=surveys_result, acl='R')
RolePermission.objects.create(role=role_analyst, datatype=clients_client, acl='L')
RolePermission.objects.create(role=role_analyst, datatype=clients_clientdata, acl='L')
RolePermission.objects.create(role=role_analyst, datatype=clients_division, acl='L')
RolePermission.objects.create(role=role_analyst, datatype=clients_role, acl='L')
RolePermission.objects.create(role=role_analyst, datatype=clients_person, acl='L')
RolePermission.objects.create(role=role_analyst, datatype=clients_squad, acl='L')

RolePermission.objects.create(role=role_administrator, datatype=questions_answer, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=questions_question, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=querylists_querylist, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=querylists_querycontent, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=schedules_task, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=schedules_schedule, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=schedules_attempt, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=surveys_anketa, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=surveys_result, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=clients_client, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=clients_clientdata, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=clients_division, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=clients_role, acl='LRCUD')
RolePermission.objects.create(role=role_administrator, datatype=clients_person, acl='M')
RolePermission.objects.create(role=role_administrator, datatype=clients_squad, acl='M')
"""
RolePermission.objects.create(role=role_, datatype=questions_answer, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=questions_question, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=querylists_querylist, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=querylists_querycontent, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=schedules_task, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=schedules_schedule, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=schedules_attempt, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=surveys_anketa, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=surveys_result, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=clients_client, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=clients_clientdata, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=clients_division, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=clients_role, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=clients_person, acl='LRCUDM')
RolePermission.objects.create(role=role_, datatype=clients_squad, acl='LRCUDM')
"""

#
#   clients Person
#
from clients.models import Person
from ..home.install import user_site1, user_sbrf1, user_sbrf2, user_freebee, user_freebee1

def add_person(user, shortname, division, roles):
    print("Adding: user={}, shortname={}, division={}".format(user, shortname, division))
    print(" roles:", ", ".join(('"{}"'.format(r) for r in roles)))
    person = Person(
        user=user,
        shortname=shortname,
        division=division,
    )
    person.save()
    person.roles.add(*roles)
    return person

site1_user = add_person(
    user=user_site1,
    shortname='Первый',
    division=division_the_site,
    roles=(role_user, role_testee,),
)

sbrf1_user = add_person(
    user=user_sbrf1,
    shortname='Николай',
    division=division_sbrf,
    roles=(role_user,),
)
sbrf1_testee = add_person(
    user=user_sbrf1,
    shortname=user_sbrf1.username,
    division=division_sbrf,
    roles=(role_testee,),
)
sbrf1_account_manager = add_person(
    user=user_sbrf1,
    shortname=role_account_manager.name,
    division=division_sbrf,
    roles=(role_account_manager,),
)
sbrf1_administrator = add_person(
    user=user_sbrf1,
    shortname=role_administrator.name,
    division=division_sbrf,
    roles=(role_administrator,),
)
sbrf1_analyst = add_person(
    user=user_sbrf1,
    shortname=role_analyst.name,
    division=division_sbrf,
    roles=(role_analyst,),
)
sbrf1_client_manager = add_person(
    user=user_sbrf1,
    shortname=role_client_manager.name,
    division=division_sbrf,
    roles=(role_client_manager,),
)
sbrf1_content_manager = add_person(
    user=user_sbrf1,
    shortname=role_content_manager.name,
    division=division_sbrf,
    roles=(role_content_manager,),
)
sbrf1_editor = add_person(
    user=user_sbrf1,
    shortname=role_editor.name,
    division=division_sbrf,
    roles=(role_editor,),
)
sbrf1_moderator = add_person(
    user=user_sbrf1,
    shortname=role_moderator.name,
    division=division_sbrf,
    roles=(role_moderator,),
)
sbrf1_schedule_manager = add_person(
    user=user_sbrf1,
    shortname=role_schedule_manager.name,
    division=division_sbrf,
    roles=(role_schedule_manager,),
)

sbrf2_user = add_person(
    user=user_sbrf2,
    shortname='Петруха',
    division=division_sbrf,
    roles=(role_testee,),
)

freebee_user =  add_person(
    user=user_freebee,
    shortname=user_freebee.username,
    division=division_freebee,
    roles=(role_user,),
)
freebee_superuser =  add_person(
    user=user_freebee,
    shortname='Супермен',
    division=division_freebee,
    roles=(
        # role_user,
        role_account_manager,
        role_administrator,
        role_analyst,
        role_client_manager,
        role_content_manager,
        role_editor,
        role_moderator,
        role_schedule_manager
    ),
)

freebee_testee =  add_person(
    user=user_freebee1,
    shortname='Пользователь',
    division=division_freebee,
    roles=(role_testee,),
)

#
#   clients Squad
#
from clients.models import Squad

def add_squad(name, shortname, description, division, members):
    print("Adding squad: name={}, shortname={}, division={}".format(name, shortname, division))
    print("     members:", ", ".join(('"{}"'.format(r) for r in members)))
    squad = Squad(
        name=name,
        shortname=shortname,
        description=description,
        division=division,
    )
    squad.save()
    squad.members.add(*members)
    return squad

squad_sbrf_users = add_squad(
    name='Весь СБЕРБАНК',
    shortname='SBRF_USERS',
    description="""Все Личности СБЕРБАНКА с ролью Пользователь""",
    division=division_sbrf,
    members=(sbrf1_user, sbrf2_user,),
)

squad_freebee_all = add_squad(
    name='Весь FreeBee',
    shortname='FREEBEE_ALL',
    description="""Все Личности FreeBee""",
    division=division_freebee,
    members=(freebee_user, freebee_superuser,),
)

squad_freebee_users = add_squad(
    name='Пользователи FreeBee',
    shortname='FREEBEE_USERS',
    description="""Все Личности FreeBee с ролью Пользователь""",
    division=division_freebee,
    members=(freebee_testee,),
)