from django.db import models


class Service(models.Model):
    service_id = models.CharField(max_length=64, default='LOCNSZDT001')
    service_name = models.CharField(max_length=64, default='IoT Service')

    max_nodes = models.IntegerField(default=9999)
    url = models.URLField(max_length=200, default='www.xiaoxiezi.net')
    description = models.CharField(max_length=3000, default='no description.')
    rule = models.CharField(max_length=3000, default='{"Desc":[{"From":16,"To":1,"Type":"enum","prefix":"地磁:","enum": {"0":"无车","1":"有车"}},{"From":12,"To":4,"Type":"enum","prefix":"类型:","enum": {"0":"检测","1":"检测","2":"心跳"}},{"From":17,"To":7,"Type":"numerical","prefix":"电量: ","suffix":"%"}]}')
    register_time = models.DateTimeField(auto_now_add=True)
    register_nodes = models.IntegerField(default=15)
    active_nodes = models.IntegerField(default=5)

    class Meta:
        ordering = ('service_id', 'service_name',)

    def __str__(self):
        return str(self.service_name)
