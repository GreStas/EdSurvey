from ..surveys import uninstall

from schedules.models import Attempt, Schedule, Task

Attempt.objects.all().delete()
for schedule in Schedule.objects.all():
    schedule.squads.all().delete()
    schedule.delete()
Task.objects.all().delete()
