from django.contrib import admin

from .models import QueryList, QueryContent


@admin.register(QueryList)
class QueryListAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


@admin.register(QueryContent)
class TestContentAdmin(admin.ModelAdmin):
    list_display = ('querylist', 'question', 'ordernum')