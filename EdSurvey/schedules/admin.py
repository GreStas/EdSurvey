from django.contrib import admin
from .models import Task, Schedule, Attempt


class ScheduleAdmin(admin.TabularInline):
    model = Schedule


class TaskAdmin(admin.ModelAdmin):
    # list_display = ('id', 'description', 'qtype')
    ordering = ('description', 'querylist')
    fieldsets = [
        (None, {'fields': ['description', 'querylist']}),
        ('Параметры', {'fields': ['attempts', 'editable', 'viewable', 'autoclose',]})
    ]
    inlines = [
        ScheduleAdmin,
    ]

admin.site.register(Task, TaskAdmin)


class AttemptAdmin(admin.ModelAdmin):
    # list_display = ('id', 'description', 'qtype')
    ordering = ('schedule', '-started')
    # fieldsets = [
    #     (None, {'fields': ['attempt', 'question', 'answer']}),
    # ]

admin.site.register(Attempt, AttemptAdmin)
