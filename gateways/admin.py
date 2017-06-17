from django.contrib import admin
from nodes.models import *
from gateways.models import *
from services.models import *

class NodeAdmin(admin.ModelAdmin):
    list_display = ('node_id', 'node_type', 'register_time')
class NodeRawDataAdmin(admin.ModelAdmin):
    list_display = ('data', 'node', 'gateway', 'time')

class GatewayAdmin(admin.ModelAdmin):
    list_display = ('gateway_id', 'gateway_name', 'gateway_type', 'register_time')
class GatewayDataAdmin(admin.ModelAdmin):
    list_display = ('data1', 'gateway', 'time')

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'service_name')

admin.site.register(LoRaNode, NodeAdmin)
admin.site.register(NodeRawData, NodeRawDataAdmin)
admin.site.register(Gateway, GatewayAdmin)
admin.site.register(GatewayData, GatewayDataAdmin)
admin.site.register(Service, ServiceAdmin)
