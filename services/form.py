from .models import Service
from django.forms import ModelForm

class ServiceInfoForm(ModelForm):
    class Meta:
        model = Service
        fields = ['service_id', 'service_name', 'max_nodes', 'url', 'description']
