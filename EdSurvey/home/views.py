from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls.base import reverse


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
            try:
                return redirect(request.GET['next'])
            except MultiValueDictKeyError:
                return redirect(reverse('homepage'))
    return render(request, 'login.html', {'form': form})

def log_out(request):
    logout(request)
    return redirect(reverse('homepage'))


def index(request):
    return render(
        request,
        'home.htm',
    )
