# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-17 09:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_auto_20170816_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_ptr', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, parent_link=True, to=settings.AUTH_USER_MODEL, verbose_name='пользователь сайта')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clients.Client')),
                ('division', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='clients.Division')),
            ],
        ),
    ]
