# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-08 15:44
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('threads', '0003_answer_points'),
        ('user', '0004_auto_20170208_1557'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnsweredNotifcation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('theanswer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='threads.answer')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.ManyToManyField(to='user.AnsweredNotifcation')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
