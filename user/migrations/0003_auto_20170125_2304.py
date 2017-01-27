# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-25 17:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20170125_2303'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='age',
            field=models.PositiveSmallIntegerField(default=18),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student',
            name='location',
            field=models.CharField(blank=True, default='', max_length=30),
        ),
    ]
