#   clients.admin
from django.contrib import admin

from .models import Client, Division, ClientData


class DivisionAdmin(admin.TabularInline):
    model = Division
    ordering = ('shortname',)
    fieldsets = [
        (None, {'fields': ['shortname', 'name',]}),
        ('Параметры', {'fields': ['public', 'private',]})
    ]


class ClientDataAdmin(admin.TabularInline):
    model = ClientData
    fieldsets = [
        (None, {'fields': ['id', 'rootdivision', 'fullname', 'address',]})
        # ('Параметры Клиента', {'fields': ['division',]})
    ]


class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ('id', 'shortname', 'name')
    inlines = [
        DivisionAdmin,
        ClientDataAdmin,
    ]

admin.site.register(Client, ClientAdmin)
