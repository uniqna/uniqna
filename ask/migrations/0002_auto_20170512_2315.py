# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-12 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='flair',
            field=models.CharField(max_length=180, null=True),
        ),
        migrations.AddField(
            model_name='question',
            name='flair_icon',
            field=models.CharField(max_length=25, null=True),
        ),
    ]