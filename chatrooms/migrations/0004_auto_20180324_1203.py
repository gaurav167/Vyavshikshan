# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-24 06:33
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatrooms', '0003_auto_20180205_2320'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='room',
            options={'base_manager_name': 'objects'},
        ),
    ]
