# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 11:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('querylists', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('finish', models.DateTimeField()),
                ('description', models.CharField(blank=True, max_length=30, null=True)),
            ],
            options={
                'verbose_name_plural': 'Расписание заданий',
                'verbose_name': 'Назначеное тестирование',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempts', models.PositiveIntegerField(default=1)),
                ('description', models.CharField(max_length=30)),
                ('querylist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='querylists.QueryList')),
            ],
            options={
                'verbose_name_plural': 'Задания на тестирование',
                'verbose_name': 'Задание на тестирование',
            },
        ),
        migrations.AddField(
            model_name='schedule',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='schedules.Task'),
        ),
    ]
