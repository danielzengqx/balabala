from rest_framework import serializers

from .models import LoRaNode, NodeRawData, ServiceData


class LoraNodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoRaNode
        fields = ('node_id', 'node_name', 'node_type', 'latitude', 'longitude',
            'Lastalive_time', 'device_status', 'device_control', 'max_data_record', 'heartbeat_interval', 'service',
            'EUI', 'DevAddr', 'AppKey', 'NwkSKey', 'AppSKey')


class NodeRawDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = NodeRawData
        fields = ('data', 'node', 'gateway')


class ServiceDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceData
        fields = ('info1', 'data1', 'node', 'gateway')
