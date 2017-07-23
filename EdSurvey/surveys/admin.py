from django.contrib import admin
from .models import Result, Attempt

# В проде не будет админки, так как это будет приложение для пользователей


class ResultAdmin(admin.TabularInline):
    model = Result


class AttemptAdmin(admin.ModelAdmin):
    # list_display = ('id', 'description', 'qtype')
    ordering = ('schedule', 'attempt')
    # fieldsets = [
    #     (None, {'fields': ['attempt', 'question', 'answer']}),
    # ]
    inlines = [
        ResultAdmin,
    ]

admin.site.register(Attempt, AttemptAdmin)
