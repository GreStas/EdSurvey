from ..home import install

#
#   clients DataType
#
#  = DataType.objects.create(
#     name='',
#     description='',
#     applabel='',
#     model='',
# )
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



#
#   clients Role
#
from clients.models import Role

allusers = Role.objects.create(
    id=1,
    name='Пользователь сайта',
    shortname='USER',
    description="Все пользователия сайта, прошедшие регистрацию, которые могут создавать свой персональный контент.",
)
editor = Role.objects.create(
    name='Редактор',
    shortname='EDITOR',
    description="Создаёт и изменяет контент",
)
content_manager = Role.objects.create(
    name='Менеджер контента',
    shortname='CONTENT_MGR',
    description="Управляет правами на контент",
)
schedule_manager = Role.objects.create(
    name='Менеджер заданий',
    shortname='SCHEDULE_MGR',
    description="Управляет заданиями и расписаниями по ним",
)
account_manager = Role.objects.create(
    name='Менеджер',
    shortname='ACCOUNT_MGR',
    description="Управляет персоналом клиента",
)
client_manager = Role.objects.create(
    name='Менеджер клиента',
    shortname='CLIENT_MGR',
    description="Управляет объектами клиента",
)
moderator = Role.objects.create(
    name='Модератор',
    shortname='MODERATOR',
    description="Видит всё, кроме ответов и управлет оргструктурой клиента",
)
analyst = Role.objects.create(
    name='Аналитик',
    shortname='ANALYST',
    description="Формирует аналитику и статистику",
)
administrator = Role.objects.create(
    name='Администратор',
    shortname='ADMINISTRATOR',
    description="Управляет правами на права на объекты",
)


#
#   clients RolePermision
#
from clients.models import RolePermission

RolePermission.objects.create(
    role = allusers,
    datatype = questions_question,
    acl = 'R'
)
RolePermission.objects.create(
    role = editor,
    datatype = questions_question,
    acl = 'LRCUD'
)
RolePermission.objects.create(
    role = moderator,
    datatype = questions_question,
    acl = 'L'
)
