from django.shortcuts import render

from .models import QueryList, QueryContent


def index(request):
    querylists = QueryList.objects.all()
    return render(
        request,
        'querylists.html',
        {'querylists': querylists},
    )
