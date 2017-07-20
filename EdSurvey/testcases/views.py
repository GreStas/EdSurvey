from django.shortcuts import render
from .models import TestCase, TestContent

def index(request):
    testcases = TestCase.objects.all()
    return render(
        request,
        'testcases.html',
        {'testcases': testcases},
    )
