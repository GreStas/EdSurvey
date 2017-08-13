from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string

from .models import QueryList, QueryContent


def index(request):
    querylists = QueryList.objects.all()
    return render(
        request,
        'querylists.html',
        {'querylists': querylists},
    )


@login_required(login_url='login')
def render_querylist_info(request, querylist):
    return render_to_string(
        'querylistinfoblock.html',
        {
            'querylist': querylist,
            'questionscnt': QueryContent.objects.all().filter(querylist=querylist).count(),
        },
    )