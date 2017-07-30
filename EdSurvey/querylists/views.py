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

def render_querylist_info(querylist):
    return render_to_string(
        'querylistinfoblock.html',
        {
            'querylist': querylist,
            'questionscnt': QueryContent.objects.all().filter(querylist=querylist).count(),
        },
    )