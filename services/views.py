from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .form import ServiceInfoForm
from .models import Service
# Create your views here.
def index(request):
	template = "service_index.html"
	context = {

	}
	return render(request, template, context)

def service_add(request):
    if request.method == 'POST':
        #check the post value
        print(request.POST)
        form = ServiceInfoForm(request.POST)
        if form.is_valid():
            print('form is valid!')
            servicename = form.cleaned_data['service_name']
            serviceid = form.cleaned_data['service_id']
            maxnodes = form.cleaned_data['max_nodes']
            url = form.cleaned_data['url']
            description = form.cleaned_data['description']
            service = Service(service_id=serviceid, service_name=servicename, max_nodes=maxnodes, url=url, description=description )
            service.save()
            return HttpResponseRedirect('/services/')
        else:
            print("form is not valid!!!")
    else:
        form = ServiceInfoForm()
    template = "service_add.html"
    context = {

    }
    return render(request, template, context)

def service_detail(request):
    template = "service_detail.html"
    context = {

    }
    return render(request, template, context)