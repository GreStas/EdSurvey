from ..questions import uninstall

from clients.models import Squad, Person, RolePermission, DataType, Role, Division, ClientData, Client


Squad.objects.all().delete()
Person.objects.all().delete()
RolePermission.objects.all().delete()
DataType.objects.all().delete()
Role.objects.all().delete()
ClientData.objects.all().delete()
Division.objects.all().delete()
Client.objects.all().delete()
