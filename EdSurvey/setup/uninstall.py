#
#   clients RolePermision
#
from clients.models import RolePermision

RolePermision.objects.all().delete()


#
#   clients Role
#
from clients.models import Role

Role.objects.all().delete()


#
#   clients DataType
#
from clients.models import DataType

DataType.objects.all().delete()