from django.db import models
from django.utils import timezone


class Gateway(models.Model):
    gateway_id = models.CharField(max_length=64, default='ffff', unique=True, primary_key=True)
    gateway_name = models.CharField(max_length=64, default='no name')
    vendor = models.CharField(max_length=64, default='Huawei')

    DEVICE_TYPE_CHOICES = (
        ('LoRa', 'LoRa'),
        ('NB-IOT', 'NB-IOT'),
        ('others', 'others'),
    )
    gateway_type = models.CharField(max_length=64, choices=DEVICE_TYPE_CHOICES, default='LoRa',)

    province = models.CharField(max_length=64, default='Guangdong',)
    city = models.CharField(max_length=64, default='Guangzhou',)
    address = models.CharField(max_length=64, default='Earth')

    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=113.957666,)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=22.523888,)

    register_time = models.DateTimeField(auto_now_add=True)
    Lastalive_time = models.DateTimeField(default=timezone.now)
    device_control = models.CharField(max_length=32, choices=(('ENABLED', 'ENABLED'), ('DISABLED', 'DISABLED')), default='ENABLED',)
    device_status = models.CharField(max_length=32, choices=(('active', 'active'), ('inactive', 'inactive')), default='active',)
    max_data_record = models.BigIntegerField(default=100000000,)

    class Meta:
        ordering = ('gateway_id', 'gateway_name', 'gateway_type', 'register_time')

    def __str__(self):
        return str(self.gateway_name)


class GatewayData(models.Model):
    data1 = models.CharField(max_length=128, default='data1')
    data2 = models.CharField(max_length=128, default='data2')
    battery = models.CharField(max_length=64, default='5%')
    gateway = models.ForeignKey('Gateway', on_delete=models.SET_NULL, blank=True, null=True,)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.data1)
