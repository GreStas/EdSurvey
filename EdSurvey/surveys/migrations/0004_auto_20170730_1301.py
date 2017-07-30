# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-30 10:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0003_auto_20170730_1112'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attempt',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='attempt',
            name='schedule',
        ),
        migrations.AlterField(
            model_name='result',
            name='attempt',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.Attempt'),
        ),
        migrations.DeleteModel(
            name='Attempt',
        ),
    ]