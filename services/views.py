from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .form import ServiceInfoForm
from .models import Service

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
            service = form.save(commit=False)
            service.save()
            return HttpResponseRedirect('/services/')
        else:
            print('form is not valid!')
            template = "service_add.html"
            context = {
                "form":form
            }
            return render(request, template, context)
    else:
        form = ServiceInfoForm()
    template = "service_add.html"
    context = {
    }
    return render(request, template, context)


def service_detail(request, service_id):
    try:
        single_service = Service.objects.get(service_id=service_id)
        print('single_service: % s' % single_service)
    except Service.DoesNotExist:
        return HttpResponse("Service with ID %s doesn't exist!" % (service_id))

    template = "service_detail.html"
    context = {
        "single_service":single_service
    }
    return render(request, template, context)


def service_modify(request, service_id):
    try:
        single_service = Service.objects.get(service_id=service_id)
    except Service.DoesNotExist:
        return HttpResponse("service with ID %s doesn't exist!" % (service_id))

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
            rule = form.cleaned_data['rule']
            Service.objects.filter(service_id=service_id).update(service_name=servicename, max_nodes=maxnodes, url=url, description=description, rule=rule)
            return HttpResponseRedirect('/services/')
        else:
            return HttpResponse("form is not valid!!!")

    else:
        form = ServiceInfoForm()

    template = "service_modify.html"
    context = {
        "single_service": single_service
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
