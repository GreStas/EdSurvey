from ..questions import uninstall

from clients.models import Squad, Person, RolePermission, DataType, Role, Division, ClientData, Client


for squad in Squad.objects.all():
    squad.members.all().delete()
    squad.delete()
for person in Person.objects.all():
    person.roles.all().delete()
    person.delete()
RolePermission.objects.all().delete()
DataType.objects.all().delete()
Role.objects.all().delete()
ClientData.objects.all().delete()
Division.objects.all().delete()
Client.objects.all().delete()
