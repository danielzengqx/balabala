from .models import Service
from django.forms import ModelForm

class ServiceInfoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(ModelForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['url'].required = False
        self.fields['description'].required = False
        self.fields['rule'].required = False

    class Meta:
        model = Service
        fields = ('service_id', 'service_name', 'max_nodes', 'url', 'description', 'rule')

    # skip unique check for service_modify function
    def validate_unique(self):
        pass
