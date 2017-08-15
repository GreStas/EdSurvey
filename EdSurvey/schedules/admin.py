from django.contrib import admin
from .models import Task, Schedule, Attempt


class ScheduleAdmin(admin.TabularInline):
    model = Schedule


class TaskAdmin(admin.ModelAdmin):
    ordering = ('name', 'querylist')
    fieldsets = [
        (None, {'fields': ['name','description', 'querylist', 'division',]}),
        ('Параметры', {'fields': ['attempts', 'editable', 'viewable', 'autoclose', 'public']})
    ]
    inlines = [
        ScheduleAdmin,
    ]

admin.site.register(Task, TaskAdmin)


class AttemptAdmin(admin.ModelAdmin):
    ordering = ('schedule', '-started')

admin.site.register(Attempt, AttemptAdmin)
