# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-26 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateways', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gateway',
            name='gateway_id',
            field=models.CharField(default='ffff', max_length=64, unique=True),
        ),
    ]