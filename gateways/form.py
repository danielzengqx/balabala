from django.forms import ModelForm

from .models import Gateway, GatewayData


class GatewayInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for item in ['latitude', 'longitude', 'address', ]:
            self.fields[item].required = False

    class Meta:
        model = Gateway
        fields = ('gateway_id', 'gateway_name', 'vendor', 'gateway_type',
            'province', 'city', 'address', 'latitude', 'longitude',
            'device_control', 'max_data_record', 'heartbeat_interval')


class GatewayDataInfoForm(ModelForm):
    class Meta:
        model = GatewayData
        fields = ('data1', 'data2', 'battery', 'gateway')
