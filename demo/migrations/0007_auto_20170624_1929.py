# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2017-06-24 19:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0006_article'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='avatar',
        ),
        migrations.RemoveField(
            model_name='user',
            name='mobile',
        ),
        migrations.RemoveField(
            model_name='user',
            name='qq',
        ),
        migrations.RemoveField(
            model_name='user',
            name='url',
        ),
    ]
