#  clients.views
from django.shortcuts import render

from .models import OWNER_NAME, OWNER_SHORTNAME, Client

# Корневой клиент всегда будет такой как надо.
try:
    client = Client.objects.get(pk=1)
    if client.name != OWNER_NAME or client.shortname != OWNER_SHORTNAME:
        client.name = OWNER_NAME
        client.shortname = OWNER_SHORTNAME
        client.save()
except:
    client = Client(
        name=OWNER_NAME,
        shortname=OWNER_SHORTNAME,
    )
    client.save()

