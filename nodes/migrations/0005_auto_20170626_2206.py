# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 14:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nodes', '0004_auto_20170626_2203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noderawdata',
            name='id',
            field=models.CharField(max_length=128, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='servicedata',
            name='id',
            field=models.CharField(max_length=128, primary_key=True, serialize=False),
        ),
    ]
