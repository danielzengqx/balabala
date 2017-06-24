from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics

from .models import Gateway, GatewayData
from .form import GatewayInfoForm, GatewayDataInfoForm
from .serializers import GatewaySerializer, GatewayDataSerializer


# Create your views here.
def index(request):
    gateways = Gateway.objects.all()
    return render_to_response("gateway_test.html", {'gateways': gateways})


def gateway_add(request):
    if request.method == 'POST':
        form = GatewayInfoForm(request.POST)
        if form.is_valid():
            gateway = form.save(commit=False)
            gateway.save()
            return HttpResponseRedirect('/gateways/')
        else:
            return HttpResponse('form wrong!')
    else:
        form = GatewayInfoForm()

    return render_to_response("gateway_test.html", {'form': form})


def gateway_detail(request, gateway_id):
    try:
        gateway = Gateway.objects.get(gateway_id=gateway_id)
    except Gateway.DoesNotExist:
        return HttpResponse("gateway with ID %s doesn't exist!" % (gateway_id))

    return render_to_response("gateway_test.html", {'gateway': gateway})


def gateway_modify(request, gateway_id):
    gateway = Gateway.objects.get(gateway_id=gateway_id)
    if request.method == 'POST':
        form = GatewayInfoForm(request.POST)
        if form.is_valid():
            gateway = form.save(commit=False)
            gateway.save()
            return HttpResponseRedirect('/gateways/')
        else:
            return HttpResponse('form wrong!')
    else:
        form = GatewayInfoForm()

    return render_to_response("gateway_test.html", {'form': form})


#@csrf_exempt
def gateway_delete(request, gateway_id):
    try:
        gateway = Gateway.objects.get(gateway_id=gateway_id)
        gateway.delete()
    except Gateway.DoesNotExist:
        return HttpResponse("gateway with ID %s doesn't exist!" % (gateway_id))
    except:
        return HttpResponse('Delete gateway %s failed!' % gateway_id)

    return HttpResponseRedirect('/gateways/')


#### REST API ###
class GatewayList(generics.ListCreateAPIView):
    queryset = Gateway.objects.all()
    serializer_class = GatewaySerializer


class GatewayDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gateway.objects.all()
    serializer_class = GatewaySerializer
