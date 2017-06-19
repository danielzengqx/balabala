# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-17 15:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gateway_id', models.CharField(default='ffff', max_length=64)),
                ('gateway_name', models.CharField(default='no name', max_length=64)),
                ('vendor', models.CharField(default='Huawei', max_length=64)),
                ('gateway_type', models.CharField(choices=[('LoRa', 'LoRa'), ('others', 'others')], default='LoRa', max_length=64)),
                ('province', models.CharField(choices=[('Guangdong', 'Guangdong'), ('Liaoning', 'Liaoning')], default='Guangdong', max_length=64)),
                ('city', models.CharField(choices=[('Guangzhou', 'Guangzhou'), ('Shenzhen', 'Shenzhen'), ('others', 'others')], default='Guangzhou', max_length=64)),
                ('address', models.CharField(default='Earth', max_length=64)),
                ('latitude', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('longitude', models.DecimalField(decimal_places=2, default=0.0, max_digits=4)),
                ('register_time', models.DateTimeField(auto_now_add=True)),
                ('Lastalive_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('device_status', models.CharField(choices=[('ENABLED', 'ENABLED'), ('DISABLED', 'DISABLED')], default='ENABLED', max_length=32)),
            ],
            options={
                'ordering': ('gateway_id', 'gateway_name', 'gateway_type', 'register_time'),
            },
        ),
        migrations.CreateModel(
            name='GatewayData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data1', models.CharField(default='data1', max_length=128)),
                ('data2', models.CharField(default='data2', max_length=128)),
                ('battery', models.CharField(default='5%', max_length=64)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('gateway', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gateways.Gateway')),
            ],
        ),
    ]