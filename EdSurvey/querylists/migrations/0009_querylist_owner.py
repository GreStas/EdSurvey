# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-26 20:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0025_auto_20170826_2302'),
        ('querylists', '0008_auto_20170825_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='querylist',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='clients.Person', verbose_name='владелец'),
            preserve_default=False,
        ),
    ]
