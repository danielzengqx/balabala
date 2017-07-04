from django.db import models
from django.utils import timezone


#from nodes.fields import ListField
from gateways.models import Gateway
from services.models import Service


class Node(models.Model):
    node_id = models.CharField(max_length=64, default='ffff', unique=True, primary_key=True)
    node_name = models.CharField(max_length=64, default='no name')

    DEVICE_TYPE_CHOICES = (
        ('sensor', 'sensor'),
        ('switch', 'switch'),
        ('buzzer', 'buzzer'),
        ('others', 'others'),
    )
    node_type = models.CharField(max_length=64, choices=DEVICE_TYPE_CHOICES, default='sensor',)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=113.957666,)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=22.523888,)

    register_time = models.DateTimeField(auto_now_add=True)
    Lastalive_time = models.DateTimeField(default=timezone.now)
    device_control = models.CharField(max_length=32, choices=(('ENABLED', 'ENABLED'), ('DISABLED', 'DISABLED')), default='ENABLED',)
    device_status = models.CharField(max_length=32, choices=(('active', 'active'), ('inactive', 'inactive')), default='active',)
    max_data_record = models.BigIntegerField(default=100000000,)
    heartbeat_interval = models.IntegerField(default=60 * 1,)
    service = models.ForeignKey('services.Service')
    #datas = ListField(max_length=100, default=[])

    class Meta:
        ordering = ('node_id', 'node_type', 'register_time')
        #abstract = True

    def __str__(self):
        return str(self.node_name)


class LoRaNode(Node):
    EUI = models.CharField(max_length=64, default='eeee', unique=True)
    DevAddr = models.CharField(max_length=64, default='ffff', unique=True)
    AppKey = models.CharField(max_length=256, default='')
    NwkSKey = models.CharField(max_length=256, default='')
    AppSKey = models.CharField(max_length=254, default='')

    class Meta:
        ordering = ('EUI', 'node_type', 'register_time')


class NodeRawData(models.Model):
    # id = models.CharField(max_length=128, primary_key=True)
    data = models.CharField(max_length=128, default='')
    node = models.ForeignKey('LoRaNode', on_delete=models.SET_NULL, blank=True, null=True,)
    gateway = models.ForeignKey('gateways.Gateway', on_delete=models.SET_NULL, blank=True, null=True,)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.data)


class ServiceData(models.Model):
    # id = models.CharField(max_length=128, primary_key=True)
    info1 = models.CharField(max_length=128, default='info1')
    info2 = models.CharField(max_length=128, default='')
    info3 = models.CharField(max_length=128, default='')

    data1 = models.CharField(max_length=128, default='')
    data2 = models.CharField(max_length=128, default='')
    data3 = models.CharField(max_length=128, default='')

    node = models.ForeignKey('LoRaNode', on_delete=models.SET_NULL, blank=True, null=True,)
    gateway = models.ForeignKey('gateways.Gateway', on_delete=models.SET_NULL, blank=True, null=True,)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.data1)
