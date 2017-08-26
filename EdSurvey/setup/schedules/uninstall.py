from ..surveys import uninstall

from schedules.models import Attempt, Schedule, Task

Attempt.objects.all().delete()
Schedule.objects.all().delete()
Task.objects.all().delete()
