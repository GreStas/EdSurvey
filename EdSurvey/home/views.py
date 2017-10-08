from django.shortcuts import render
from django.template.loader import render_to_string


def contacts(request):
    return render(
        request,
        'contacts.html',
    )


def manuals(request):
    return render(
        request,
        'manuals.html',
    )


def index(request):
    if hasattr(request, 'person'):
        print("request.person in home.views.index = ", request.person)
    else:
        print("request.person isn't in home.views.index")
    return render(
        request,
        'home.htm',
    )
