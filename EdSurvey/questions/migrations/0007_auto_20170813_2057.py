# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-13 17:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0006_question_division'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='division',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clients.Division'),
        ),
    ]
