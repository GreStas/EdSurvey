# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 18:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0012_auto_20170813_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='division',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clients.Division'),
        ),
    ]
