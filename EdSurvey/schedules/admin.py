from django.contrib import admin
from .models import Task, Schedule


class ScheduleAdmin(admin.TabularInline):
    model = Schedule


class TaskAdmin(admin.ModelAdmin):
    # list_display = ('id', 'description', 'qtype')
    ordering = ('description', 'testcase')
    fieldsets = [
        (None, {'fields': ['description', 'testcase', 'attempts']}),
    ]
    inlines = [
        ScheduleAdmin,
    ]

admin.site.register(Task, TaskAdmin)