# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-12 07:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedules', '0005_auto_20170806_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='name',
            field=models.CharField(default='.', max_length=30),
            preserve_default=False,
        ),
    ]