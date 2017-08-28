from django.contrib.auth.models import User

# Создать ключевых пользователей и группы
user_site1 = User.objects.create_user(
    username = 'site1',
    first_name = 'Вася',
    last_name = 'Пупкин',
    email = 'site1@edsurvey.org',
    is_staff = False,
    is_active = True,
)
user_site1.set_password("zxasqw12")
user_site1.save()

user_sbrf1 = User.objects.create_user(
    username = 'sbrf1',
    first_name = 'Николай',
    last_name = 'Кристофари',
    email = 'sbrf1@sbrf.com',
    is_staff = False,
    is_active = True,
)
user_sbrf1.set_password('qwer1234')
user_sbrf1.save()

user_freebee = User.objects.create_user(
    username='freebee',
    first_name='Иван',
    last_name='Халявин',
    email='freebee@edsurvey.org',
    is_staff=False,
    is_active=True,
)
user_freebee.set_password("zxasqw12")
user_freebee.save()
