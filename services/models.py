from django.db import models


class Service(models.Model):
    service_id = models.CharField(max_length=64, default='LOCNSZDT001')
    service_name = models.CharField(max_length=64, default='IoT Service')

    max_nodes = models.IntegerField(default=9999)
    url = models.URLField(max_length=200, default='www.iot.com')
    description = models.CharField(max_length=3000, default='no description.')

    class Meta:
        ordering = ('service_id', 'service_name',)

    def __str__(self):
        return str(self.service_name)
