from django.forms import ModelForm

from .models import LoRaNode, NodeRawData, ServiceData


class LoRaNodeInfoForm(ModelForm):
    class Meta:
        model = LoRaNode
        fields = ('node_id', 'node_name', 'node_type',
            'latitude', 'longitude', 'device_control', 'max_data_record', 'heartbeat_interval',
            'service', 'EUI', 'DevAddr', 'NwkSKey', 'AppSKey')


class NodeRawDataInfoForm(ModelForm):
    class Meta:
        model = NodeRawData
        fields = ('data', 'node', 'gateway')


class ServiceDataInfoForm(ModelForm):
    class Meta:
        model = ServiceData
        fields = ('info1', 'data1', 'node', 'gateway')
