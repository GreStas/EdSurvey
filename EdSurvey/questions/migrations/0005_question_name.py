# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-12 07:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20170806_1853'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='name',
            field=models.CharField(default='вопрос', max_length=30),
            preserve_default=False,
        ),
    ]
