from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls.base import reverse

from clients.models import Person


def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST.get('username', ''),
            password=request.POST.get('password', ''),
        )
        if user is not None:
            login(request, user)
            persons = Person.objects.filter(user=user)
            cnt = len(persons)
            if cnt < 1:
                logout(request)
                raise ObjectDoesNotExist('С пользователем не связано ни одной личности')
            elif cnt == 1:
                active_person = persons[0]
            else:
                messages.add_message(request, messages.WARNING, "Sorry, MultiPerson is under construction.")
                active_person = persons[0].id
            request.session['person_id'] = active_person.id
            try:
                return redirect(request.GET['next'])
            except MultiValueDictKeyError:
                return redirect(reverse('homepage'))
    return render(request,
                  'login.html',
                  {
                      'form': form,
                  },)

def log_out(request):
    print("request.person in home.view.log_out = ", request.person)
    logout(request)
    # try:
    #     del request.session['person_id']
    #     del request.person
    # except KeyError:
    #     pass
    # del request.session['role_id']
    return redirect(reverse('homepage'))


def index(request):
    if hasattr(request, 'person'):
        print("request.person in home.views.index = ", request.person)
    else:
        print("request.person isn't in home.views.index")
    return render(
        request,
        'home.htm',
    )
