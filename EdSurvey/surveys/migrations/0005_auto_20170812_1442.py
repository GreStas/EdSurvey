# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-12 11:42
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0004_anketa_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anketa',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]
