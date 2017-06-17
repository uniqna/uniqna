# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-06-17 07:45
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('threads', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Answered',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('theanswer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='writted_answer', to='threads.Answer')),
            ],
            options={
                'ordering': ['-read'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=False)),
                ('object_id', models.IntegerField()),
                ('notification_type', models.CharField(max_length=50)),
                ('notification_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('content', models.CharField(max_length=300)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.ManyToManyField(related_name='answered_questions', to='user.Answered')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_name', models.CharField(default='', max_length=15)),
                ('bio', models.CharField(blank=True, default='', max_length=240)),
                ('course', models.CharField(choices=[('B.Tech', 'B.Tech'), ('M.Tech', 'M.Tech'), ('F.Tech', 'F.Tech'), ('B.Law', 'B.Law')], default='B.Tech', max_length=6)),
                ('school', models.CharField(choices=[('SCSE', 'SCSE'), ('SENSE', 'SENSE'), ('SAS', 'SAS'), ('SELECT', 'SELECT'), ('SMBS', 'SMBS'), ('VITBS', 'VITBS'), ('VITSOL', 'VITSOL'), ('VFIT', 'VFIT'), ('V-SPARC', 'V-SPARC'), ('SBST', 'SBST'), ('SCALE', 'SCALE'), ('SCOPE', 'SCOPE'), ('SITE', 'SITE'), ('SMEC', 'SMEC'), ('SSL', 'SSL'), ('LAW', 'LAW')], default='SCSE', max_length=6)),
                ('grad_year', models.CharField(choices=[('2017', '2017'), ('2018', '2018'), ('2019', '2019'), ('2020', '2020')], default='2020', max_length=6)),
                ('university', models.CharField(choices=[('Vellore Institute of Technology, Chennai', 'Vellore Institute of Technology, Chennai'), ('Vellore Institute of Technology, Vellore', 'Vellore Institute of Technology, Vellore')], max_length=100)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
