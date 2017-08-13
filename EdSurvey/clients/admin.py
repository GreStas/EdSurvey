#   clients.admin
from django.contrib import admin

from .models import Client, Division


class DivisionAdmin(admin.TabularInline):
    model = Division
    # list_display = ('id', 'client', 'shortname', 'name')
    ordering = ('shortname',)
    fieldsets = [
        (None, {'fields': ['shortname', 'name',]}),
        ('Параметры', {'fields': ['public', 'private',]})
    ]


class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ('id', 'shortname', 'name')
    inlines = [
        DivisionAdmin,
    ]

admin.site.register(Client, ClientAdmin)
