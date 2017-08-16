# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-16 11:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0007_delete_clientdata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_ptr', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, parent_link=True, to='clients.Client')),
                ('fullname', models.CharField(max_length=120, verbose_name='полное наименование')),
                ('address', models.TextField(verbose_name='почтовый адрес')),
                ('rootdivision', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.Division', verbose_name='корневая организация')),
            ],
            options={
                'verbose_name_plural': 'Дополнительная информация о Клиентах',
                'verbose_name': 'Дополнительная информация о Клиенте',
            },
        ),
    ]
