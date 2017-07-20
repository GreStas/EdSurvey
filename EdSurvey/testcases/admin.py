from django.contrib import admin
from .models import TestCase, TestContent


@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')


@admin.register(TestContent)
class TestContentAdmin(admin.ModelAdmin):
    list_display = ('testcase', 'question', 'ordernum')