from django.contrib import admin
from .models import Attempt, Result, ResultRB, ResultCB, ResultLL

# В проде не будет админки, так как это будет приложение для пользователей


class ResultAdmin(admin.ModelAdmin):
    model = Result


class ResultRBAdmin(admin.TabularInline):
    model = ResultRB


class ResultCBAdmin(admin.TabularInline):
    model = ResultCB


class ResultLLAdmin(admin.TabularInline):
    model = ResultLL


class AttemptAdmin(admin.ModelAdmin):
    # list_display = ('id', 'description', 'qtype')
    ordering = ('schedule', 'attempt')
    # fieldsets = [
    #     (None, {'fields': ['attempt', 'question', 'answer']}),
    # ]
    inlines = [
        ResultRBAdmin,
        ResultCBAdmin,
        ResultLLAdmin,
    ]

admin.site.register(Attempt, AttemptAdmin)
