from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.urls.base import reverse


def log_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        # form = AuthenticationForm(request.POST)
        # if form.is_valid():
        #     user = authenticate(
        #         request,
        #         username=form.cleaned_data('username'),
        #         password=form.cleaned_data('password'),
        #     )
        user = authenticate(
            request,
            username=request.POST.get('username', ''),
            password=request.POST.get('password', ''),
        )
        if user is not None:
            login(request, user)
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
