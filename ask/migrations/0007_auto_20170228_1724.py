# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-28 11:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0006_auto_20170228_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.CharField(default='anonymous', max_length=100),
        ),
        migrations.AlterField(
            model_name='question',
            name='downs',
            field=models.ManyToManyField(blank=True, related_name='question_downvotes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='question',
            name='points',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(blank=True, to='ask.tag'),
        ),
        migrations.AlterField(
            model_name='question',
            name='ups',
            field=models.ManyToManyField(blank=True, related_name='question_upvotes', to=settings.AUTH_USER_MODEL),
        ),
    ]