# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-24 05:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_remove_service_rule'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='rule',
            field=models.CharField(default='{"Desc":[{"From":16,"To":1,"Type":"enum","prefix":"地磁:","enum": {"0":"无车","1":"有车"}},{"From":12,"To":4,"Type":"enum","prefix":"类型:","enum": {"0":"检测","1":"检测","2":"心跳"}},{"From":17,"To":7,"Type":"numerical","prefix":"电量: ","suffix":"%"}]}', max_length=3000),
        ),
    ]