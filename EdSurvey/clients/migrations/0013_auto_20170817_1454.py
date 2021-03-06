# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 11:54
from __future__ import unicode_literals

import clients.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0008_alter_user_username_max_length'),
        ('clients', '0012_auto_20170817_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='название')),
                ('shortname', models.CharField(max_length=15, verbose_name='абревиатура')),
                ('description', models.TextField(verbose_name='описание')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.Group', verbose_name='стандартная группа')),
            ],
            options={
                'verbose_name': 'роль',
                'verbose_name_plural': 'роли',
            },
        ),
        migrations.AlterField(
            model_name='person',
            name='shortname',
            field=models.CharField(max_length=15, verbose_name='aka'),
        ),
        migrations.AlterUniqueTogether(
            name='person',
            unique_together=set([('user', 'shortname')]),
        ),
    ]
