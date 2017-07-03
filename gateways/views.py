from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from datetime import datetime
import re

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics

from .models import Gateway, GatewayData
from .form import GatewayInfoForm, GatewayDataInfoForm
from .serializers import GatewaySerializer, GatewayDataSerializer


# Create your views here.
def index(request):
    gateways = Gateway.objects.all()
    return render_to_response("gateway_index.html", {'gateways': gateways})


def gateway_add(request):
    if request.method == 'POST':
        form = GatewayInfoForm(request.POST)
        if form.is_valid():
            if Gateway.objects.filter(gateway_id=form.cleaned_data['gateway_id']):
                return HttpResponse("gateway with ID %s exist!" % (form.cleaned_data['gateway_id']))

            gateway = form.save(commit=False)
            gateway.save()
            return HttpResponseRedirect('/gateways/')
        else:
            return HttpResponse("form is not valid!!!")
    else:
        form = GatewayInfoForm()

    return render_to_response("gateway_test.html", {'form': form})


def gateway_detail(request, gateway_id):
    try:
        gateway = Gateway.objects.get(gateway_id=gateway_id)
    except Gateway.DoesNotExist:
        return HttpResponse("gateway with ID %s doesn't exist!" % (gateway_id))

    try:
        gateway_datas = gateway.gatewaydata_set.all().order_by('-time')
    except:
        return HttpResponse("Get data filed!\n")

    gatewaydata_update(gateway_id)
    return render_to_response("gateway_test.html", {'gateway': gateway, 'gateway_datas': gateway_datas})


def gateway_modify(request, gateway_id):
    try:
        gateway = Gateway.objects.get(gateway_id=gateway_id)
    except Gateway.DoesNotExist:
        return HttpResponse("gateway with ID %s doesn't exist!" % (gateway_id))

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


def gatewaydata_list(request, gateway_id):
    try:
        gateway = Gateway.objects.get(gateway_id=gateway_id)
    except Gateway.DoesNotExist:
        return HttpResponse("gateway with ID %s doesn't exist!" % (gateway_id))

    try:
        datas = gateway.gatewaydata_set.all()

    except:
        return HttpResponse("Get data filed!\n")

    return render_to_response("gateway_test.html", {'datas': datas})


def gatewaydata_detail(request, gateway_id, pk_id):
    try:
        gateway = Gateway.objects.get(gateway_id=gateway_id)
    except Gateway.DoesNotExist:
        return HttpResponse("gateway with ID %s doesn't exist!" % (gateway_id))

    try:
        data = gateway.gatewaydata_set.get(pk=pk_id)
    except Gateway.DoesNotExist:
        return HttpResponse("gateway with ID %s hasn't data with pk: %s!" % (gateway_id, pk_id))

    except:
        return HttpResponse("Get data filed!\n")

    return render_to_response("gateway_test.html", {'data': data})


def gatewaydata_update(gateway_id):
    try:
        gateway = Gateway.objects.get(gateway_id=gateway_id)
    except Gateway.DoesNotExist:
        print("gateway with ID %s doesn't exist!\n" % (gateway_id))
        return 0

    old_data = gateway.gatewaydata_set.order_by('-time')[gateway.max_data_record:]
    for data in old_data:
        try:
            data.delete()
        except:
            print("delete date fail!\n")

    return 1


#### REST API ###
class GatewayList(generics.ListCreateAPIView):
    queryset = Gateway.objects.all()
    serializer_class = GatewaySerializer


class GatewayDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Gateway.objects.all()
    serializer_class = GatewaySerializer


class GatewayDataList(generics.ListCreateAPIView):
    queryset = GatewayData.objects.all()
    serializer_class = GatewayDataSerializer


class GatewayDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = GatewayData.objects.all()
    serializer_class = GatewayDataSerializer
