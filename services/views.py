from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from .form import ServiceInfoForm
from .models import Service
# Create your views here.
def index(request):
    all_services = Service.objects.all
    template = "service_index.html"
    context = {
        "all_services": all_services,
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

def service_detail(request, service_id):
    single_service = Service.objects.get(service_id=service_id)
    print('single_service: % s' % single_service)
    template = "service_detail.html"
    context = {
        "single_service":single_service
    }
    return render(request, template, context)

def service_modify(request, service_id):
    single_service = Service.objects.get(service_id=service_id)
    if request.method == 'POST':
        #check the post value
        print(request.POST)
        form = ServiceInfoForm(request.POST)
        if form.is_valid():
            print('form is valid!')
            servicename = form.cleaned_data['service_name']
            maxnodes = form.cleaned_data['max_nodes']
            url = form.cleaned_data['url']
            description = form.cleaned_data['description']
            single_service.service_name = servicename
            single_service.max_nodes = maxnodes
            single_service.url = url
            single_service.description = description
            single_service.save()
            return HttpResponseRedirect('/services/')
        else:
            print("form is not valid!!!")
    else:
        form = ServiceInfoForm()
    template = "service_modify.html"
    context = {
        "single_service": single_service
    }
    return render(request, template, context)
