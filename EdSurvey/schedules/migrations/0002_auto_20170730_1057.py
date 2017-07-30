# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='autoclose',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='task',
            name='editable',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='task',
            name='viewable',
            field=models.BooleanField(default=False),
        ),
    ]
