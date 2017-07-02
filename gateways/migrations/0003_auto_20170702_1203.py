# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-02 04:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gateways', '0002_auto_20170626_2153'),
    ]

    operations = [
        migrations.AddField(
            model_name='gateway',
            name='device_control',
            field=models.CharField(choices=[('ENABLED', 'ENABLED'), ('DISABLED', 'DISABLED')], default='ENABLED', max_length=32),
        ),
        migrations.AlterField(
            model_name='gateway',
            name='city',
            field=models.CharField(default='Guangzhou', max_length=64),
        ),
        migrations.AlterField(
            model_name='gateway',
            name='device_status',
            field=models.CharField(choices=[('active', 'active'), ('inactive', 'inactive')], default='active', max_length=32),
        ),
        migrations.AlterField(
            model_name='gateway',
            name='province',
            field=models.CharField(default='Guangdong', max_length=64),
        ),
    ]
