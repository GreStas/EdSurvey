# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-17 06:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0003_auto_20170715_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='qtype',
            field=models.CharField(choices=[('RB', 'Один из ...'), ('CB', 'Несколько из ...'), ('LL', 'Путанка')], default='RB', max_length=2),
        ),
    ]
