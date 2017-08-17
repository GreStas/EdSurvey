#   clients.admin
from django.contrib import admin

from .models import Client, Division, ClientData, Person, Role


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
    ]


class ClientAdmin(admin.ModelAdmin):
    model = Client
    list_display = ('id', 'shortname', 'name')
    inlines = [
        DivisionAdmin,
        ClientDataAdmin,
    ]

admin.site.register(Client, ClientAdmin)


class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_display = ('user', 'shortname',)

admin.site.register(Person, PersonAdmin)


class RoleAdmin(admin.ModelAdmin):
    model = Role
    list_display = ('group','name', 'shortname', 'description')

admin.site.register(Role, RoleAdmin)
