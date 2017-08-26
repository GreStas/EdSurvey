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
    description='Формулировка и свойства вопроса',
    applabel='questions',
    model='Question',
)
questions_answer = DataType.objects.create(
    name='Ответ',
    description='Формулировка и свойства ответа',
    applabel='questions',
    model='Answer',
)

querylists_querylist = DataType.objects.create(
        name='Опросный лист',
        description='Опросный лист',
        applabel='querylists',
        model='QueryList',
    )
querylists_querycontent = DataType.objects.create(
    name='Список вопросов',
    description='Вопросы в опросном листе',
    applabel='querylists',
    model='QueryContent',
)
"""
 = DataType.objects.create(
    name='',
    description='',
    applabel='',
    model='',
)
"""


#
#   clients Role
#
from clients.models import Role

role_user = Role.objects.create(
    id=1,
    name='Пользователь',
    shortname='USER',
    description="""Все пользователия сайта, прошедшие регистрацию, которые могут создавать свой персональный контент.""",
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

RolePermission.objects.create(
    role = role_user,
    datatype = questions_question,
    acl = 'R'
)
RolePermission.objects.create(
    role = role_editor,
    datatype = questions_question,
    acl = 'LRCUD'
)
RolePermission.objects.create(
    role = role_moderator,
    datatype = questions_question,
    acl = 'L'
)


#
#   clients Person
#
from clients.models import Person
from ..home.install import user_site1, user_sbrf1

site1_user = Person.objects.create(
    user=user_site1,
    shortname='Первый',
    division=division_the_site,
    role=role_user,
)

sbrf1_user = Person.objects.create(
    user=user_sbrf1,
    shortname='Николай',
    division=division_sbrf,
    role=role_user,
)
sbrf1_ = Person.objects.create(
    user=user_sbrf1,
    shortname=role_account_manager.name,
    division=division_sbrf,
    role=role_account_manager,
)
sbrf1_administrator = Person.objects.create(
    user=user_sbrf1,
    shortname=role_administrator.name,
    division=division_sbrf,
    role=role_administrator,
)
sbrf1_analyst = Person.objects.create(
    user=user_sbrf1,
    shortname=role_analyst.name,
    division=division_sbrf,
    role=role_analyst,
)
sbrf1_client_manager = Person.objects.create(
    user=user_sbrf1,
    shortname=role_client_manager.name,
    division=division_sbrf,
    role=role_client_manager,
)
sbrf1_content_manager = Person.objects.create(
    user=user_sbrf1,
    shortname=role_content_manager.name,
    division=division_sbrf,
    role=role_content_manager,
)
sbrf1_editor = Person.objects.create(
    user=user_sbrf1,
    shortname=role_editor.name,
    division=division_sbrf,
    role=role_editor,
)
sbrf1_moderator = Person.objects.create(
    user=user_sbrf1,
    shortname=role_moderator.name,
    division=division_sbrf,
    role=role_moderator,
)
sbrf1_schedule_manager = Person.objects.create(
    user=user_sbrf1,
    shortname=role_schedule_manager.name,
    division=division_sbrf,
    role=role_schedule_manager,
)


#
#   clients Squad
#
from clients.models import Squad