#   clients.admin
from django.contrib import admin

from .models import Client, Division, ClientData, Person, Role, Squad, RolePermision


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


class RolePermissionAdmin(admin.TabularInline):
    model = RolePermision
    extra = 2  # how many rows to show


class RoleAdmin(admin.ModelAdmin):
    model = Role
    # list_display = ('group','name', 'shortname', 'description')
    list_display = ('name', 'shortname', 'description')
    inlines = [
        RolePermissionAdmin,
    ]


admin.site.register(Role, RoleAdmin)


class SquadAdmin(admin.ModelAdmin):
    model = Squad
    # list_display = ('group','name', 'shortname', 'description')
    # name = models.CharField('название', max_length=30)
    # shortname = models.CharField('абревиатура', max_length=15)
    # discription = models.TextField('описание', null=True, blank=True)
    # division = models.ForeignKey(Division)
    # manager = models.ForeignKey(Person, default=get_admin_user, verbose_name='менеджер группы')

admin.site.register(Squad, SquadAdmin)
