"""
from schedules.models import Schedule, Task, Attempt
from surveys.views import generate_result_list
attempt = Attempt.objects.get(pk=3)
generate_result_list(attempt)
"""
from django.test import TestCase

# Create your tests here.
