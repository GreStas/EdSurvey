# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-25 15:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0010_auto_20170825_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='public',
            field=models.BooleanField(default=False, verbose_name='публичное'),
        ),
    ]