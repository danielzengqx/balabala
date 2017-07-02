from django.forms import ModelForm

from .models import Gateway, GatewayData


class GatewayInfoForm(ModelForm):
    class Meta:
        model = Gateway
        fields = ('gateway_id', 'gateway_name', 'vendor', 'gateway_type',
            'province', 'city', 'address', 'Lastalive_time', 'device_status', 'device_control')


class GatewayDataInfoForm(ModelForm):
    class Meta:
        model = GatewayData
        fields = ('data1', 'data2', 'battery', 'gateway')
