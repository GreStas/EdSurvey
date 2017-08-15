# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 18:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_auto_20170813_1559'),
        ('querylists', '0005_auto_20170812_1035'),
    ]

    operations = [
        migrations.AddField(
            model_name='querylist',
            name='division',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='clients.Division'),
        ),
        migrations.AddField(
            model_name='querylist',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
