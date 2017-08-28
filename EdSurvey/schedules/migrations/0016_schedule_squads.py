# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-28 19:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0028_auto_20170828_1816'),
        ('schedules', '0015_auto_20170828_1854'),
    ]

    operations = [
        migrations.AddField(
            model_name='schedule',
            name='squads',
            field=models.ManyToManyField(blank=True, to='clients.Squad', verbose_name='назначение'),
        ),
    ]