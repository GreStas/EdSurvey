# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-25 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0021_auto_20170825_1429'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='название'),
        ),
        migrations.AlterField(
            model_name='role',
            name='shortname',
            field=models.CharField(max_length=15, unique=True, verbose_name='абревиатура'),
        ),
    ]
