# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-05 07:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20170605_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='subtitle',
            field=models.CharField(default=models.TextField(), max_length=200),
        ),
    ]