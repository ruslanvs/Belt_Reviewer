# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-27 03:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('belt_reviewer', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='decs',
            new_name='desc',
        ),
        migrations.RenameField(
            model_name='book',
            old_name='users',
            new_name='user',
        ),
    ]
