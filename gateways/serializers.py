from rest_framework import serializers
from .models import Gateway, GatewayData


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = ('gateway_id', 'gateway_name', 'vendor', 'gateway_type',
            'province', 'city', 'address', 'register_time',
            'Lastalive_time', 'device_status', 'device_control', 'max_data_record', 'heartbeat_interval')


class GatewayDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatewayData
        fields = ('data1', 'data2', 'battery', 'gateway', 'time')
