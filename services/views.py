from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .form import ServiceInfoForm
from .models import Service
from nodes.models import LoRaNode

### REST API ###
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Service
from .serializers import ServiceSerializer
from rest_framework import generics

# Create your views here.
def index(request):
    all_services = Service.objects.all()

    loranodes = ''
    for service in all_services:
        try:
            loranodes = service.node_set.all().order_by('-register_time')
        except:
            print("Get loranodes filed!\n")

        register_nodes = 0
        active_nodes = 0
        for node in loranodes:
            register_nodes += 1
            if node.device_status == 'active':
                active_nodes += 1
        service.register_nodes =  register_nodes
        service.active_nodes = active_nodes
        service.save()

    template = "service_index.html"
    context = {
        "all_services": all_services,
        'loranodes': loranodes,
	}
    return render(request, template, context)


def service_add(request):
    template = "service_add.html"
    if request.method == 'POST':
        #check the post value
        print(request.POST)
        form = ServiceInfoForm(request.POST)
        if form.is_valid():
            if Service.objects.filter(service_id=form.cleaned_data['service_id']):
                print('service_id already exist!')
                return HttpResponse("Service with ID %s already exist!" % form.cleaned_data['service_id'])
            print('form is valid!')
            service = form.save(commit=False)
            service.save()
            return HttpResponseRedirect('/services/')
        else:
            print('form is not valid!')
            context = {
                "form":form
            }
            return render(request, template, context)
    else:
        form = ServiceInfoForm()
        context = {}
        return render(request, template, context)


def service_detail(request, service_id):
    try:
        single_service = Service.objects.get(service_id=service_id)
        print('single_service: % s' % single_service)
    except Service.DoesNotExist:
        return HttpResponse("Service with ID %s doesn't exist!" % (service_id))

    loranodes = ''
    try:
        loranodes = single_service.loranode_set.all().order_by('-register_time')
    except:
        print("Get loranodes filed!\n")

    register_nodes = 0
    active_nodes = 0
    for node in loranodes:
        register_nodes += 1
        if node.device_status == 'active':
            active_nodes += 1
    single_service.register_nodes =  register_nodes
    single_service.active_nodes = active_nodes
    single_service.save()

    #service_nodes = LoRaNode.objects.filter(service=service_id)

    template = "service_detail.html"
    context = {
        "single_service":single_service,
        "service_nodes":loranodes
    }
    return render(request, template, context)


def service_modify(request, service_id):
    try:
        single_service = Service.objects.get(service_id=service_id)
    except Service.DoesNotExist:
        return HttpResponse("service with ID %s doesn't exist!" % (service_id))

    template = "service_modify.html"
    if request.method == 'POST':
        #check the post value
        print(request.POST)
        form = ServiceInfoForm(request.POST, instance=single_service)
        if form.is_valid():
            print('form is valid!')
            #servicename = form.cleaned_data['service_name']
            #maxnodes = form.cleaned_data['max_nodes']
            #url = form.cleaned_data['url']
            #description = form.cleaned_data['description']
            #rule = form.cleaned_data['rule']
            #Service.objects.filter(service_id=service_id).update(service_name=servicename, max_nodes=maxnodes, url=url, description=description, rule=rule)
            single_service = form.save(commit=False)
            single_service.save()
            return HttpResponseRedirect('/services/')
        else:
            print('form is not valid!')
            context = {
                "form": form,
            }
            return render(request, template, context)

    else:
        form = ServiceInfoForm()
        context = {
            "single_service": single_service,
            "form": form,
        }
    return render(request, template, context)


@csrf_exempt
def service_delete(request, service_id):
    try:
        print('Delete the service: %s now!' % service_id)
        service = Service.objects.get(service_id=service_id)
        service.delete()
    except Service.DoesNotExist:
        return HttpResponse("Service with ID %s doesn't exist!" % (service_id))
    except:
        return HttpResponse('Delete service %s failed!' % service_id)

    return HttpResponseRedirect('/services/')


#### REST API ###
class ServiceList(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
