# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-17 17:27
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=15, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('metatype', models.CharField(default='question', max_length=20)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
                ('answers', models.IntegerField(default=0)),
                ('author', models.CharField(default='anonymous', max_length=100)),
                ('created_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('hot', models.DecimalField(blank=True, decimal_places=7, default=1000.123, max_digits=11)),
                ('points', models.IntegerField(default=1)),
                ('solved', models.BooleanField(default=False)),
                ('flair_icon', models.CharField(max_length=25, null=True)),
                ('flair', models.CharField(max_length=180, null=True)),
                ('channels', models.ManyToManyField(blank=True, to='post.Channel')),
                ('downs', models.ManyToManyField(blank=True, related_name='question_downvotes', to=settings.AUTH_USER_MODEL)),
                ('ups', models.ManyToManyField(blank=True, related_name='question_upvotes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
