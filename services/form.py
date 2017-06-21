from .models import Service
from django import forms

class ServiceInfoForm(forms.Form):
    service_id = forms.CharField(max_length=64)
    service_name = forms.CharField(max_length=64)

    max_nodes = forms.IntegerField()
    url = forms.URLField(max_length=200,required=False)
    description = forms.CharField(max_length=3000, required=False)
