from django.shortcuts import render


def index(request):
    if hasattr(request, 'person'):
        print("request.person in home.views.index = ", request.person)
    else:
        print("request.person isn't in home.views.index")
    return render(
        request,
        'home.htm',
    )
