# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 11:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_clientdata'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ClientData',
        ),
    ]