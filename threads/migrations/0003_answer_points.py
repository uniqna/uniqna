# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-08 10:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('threads', '0002_auto_20170202_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='points',
            field=models.IntegerField(default=0),
        ),
    ]
