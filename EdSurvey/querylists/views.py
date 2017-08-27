from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.template.loader import render_to_string

from .models import QueryList, QueryContent
from clients.models import Person, get_active_person, has_permission


@login_required(login_url='login')
def index(request):
    person = get_active_person(request)
    querylists = QueryList.objects.perm(person=person, acl='L')
    return render(
        request,
        'querylists.html',
        {'querylists': querylists},
    )


@login_required(login_url='login')
def render_querylist_info(request, querylist, perm=False):
    """    Отображение блока информации об опроснике и количесве вопросов, включённых в него
    Может учитывать права текущей Личности - perm=True
    Возможность показать подробную информацию определяется в предствалении, которое использует эту функцию.
    :param request:
    :param querylist:
    :param perm: признак необходимости учитывать права
    :return:
    """
    person = get_active_person(request)

    def render_info_block():
        if has_permission(person=person, applabel='querylists', model='QueryContent', acl='L'):
            questionscnt = QueryContent.objects.all().filter(querylist=querylist).count(),
        else:
            questionscnt = None
        return render_to_string('querylistinfoblock.html',
                                {'querylist': querylist,
                                 'questionscnt': questionscnt,},)

    if perm:
        if has_permission(person=person, applabel='querylists', model='QueryList', acl='R'):
            return render_info_block()
        else:
            return render_to_string('emptyinfoblock.html', {'notice': 'информация по анкете отсутсвует'})
    else:
        return render_info_block()
