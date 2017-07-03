from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from datetime import datetime
import re
import requests

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import generics

from .models import LoRaNode, NodeRawData, ServiceData
from .form import LoRaNodeInfoForm, NodeRawDataInfoForm, ServiceDataInfoForm
from .serializers import LoraNodeSerializer, NodeRawDataSerializer, ServiceDataSerializer
from gateways.models import Gateway


def index(request):
    all_nodes = LoRaNode.objects.order_by('node_id')
    return render_to_response("node_index.html", {'all_nodes': all_nodes})


def loranode_add(request):
    if request.method == 'POST':
        form = LoRaNodeInfoForm(request.POST)
        if form.is_valid():
            if LoRaNode.objects.filter(node_id=form.cleaned_data['node_id']):
                return HttpResponse("node with ID %s exist!" % (form.cleaned_data['node_id']))

            loranode = form.save(commit=False)
            loranode.save()
            return HttpResponseRedirect('/nodes/')
        else:
            return HttpResponse("form is not valid!!!")
    else:
        form = LoRaNodeInfoForm()

    return render_to_response("node_add.html", {'form': form})


def loranode_detail(request, node_id):
    try:
        loranode = LoRaNode.objects.get(node_id=node_id)
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s doesn't exist!" % (node_id))

    return render_to_response("node_test.html", {'loranode': loranode})


def loranode_modify(request, node_id):
    try:
        loranode = LoRaNode.objects.get(node_id=node_id)
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s doesn't exist!" % (node_id))

    if request.method == 'POST':
        form = LoRaNodeInfoForm(request.POST)
        if form.is_valid():
            loranode = form.save(commit=False)
            loranode.save()
            return HttpResponseRedirect('/nodes/')
        else:
            return HttpResponse('form wrong!')
    else:
        form = LoRaNodeInfoForm()

    return render_to_response("node_test.html", {'form': form})


@csrf_exempt
def loranode_delete(request, node_id):
    try:
        loranode = LoRaNode.objects.get(node_id=node_id)
        loranode.delete()
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s doesn't exist!" % (node_id))
    except:
        return HttpResponse('Delete loranode %s failed!' % node_id)

    return HttpResponseRedirect('/nodes/')

def rawdata_list(request, node_id):
    try:
        loranode = LoRaNode.objects.get(node_id=node_id)
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s doesn't exist!" % (node_id))

    try:
        datas = loranode.noderawdata_set.all()

    except:
        return HttpResponse("Get data filed!\n")

    return render_to_response("node_test.html", {'datas': datas})


def rawdata_detail(request, node_id, pk_id):
    try:
        loranode = LoRaNode.objects.get(node_id=node_id)
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s doesn't exist!" % (node_id))

    try:
        data = loranode.noderawdata_set.get(pk=pk_id)
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s hasn't data with pk: %s!" % (node_id, pk_id))

    except:
        return HttpResponse("Get data filed!\n")

    return render_to_response("node_test.html", {'data': data})

def servicedata_list(request, node_id):
    try:
        loranode = LoRaNode.objects.get(node_id=node_id)
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s doesn't exist!" % (node_id))

    try:
        datas = loranode.servicedata_set.all()

    except:
        return HttpResponse("Get data filed!\n")

    return render_to_response("node_test.html", {'datas': datas})


def servicedata_detail(request, node_id, pk_id):
    try:
        loranode = LoRaNode.objects.get(node_id=node_id)
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s doesn't exist!" % (node_id))

    try:
        data = loranode.servicedata_set.get(pk=pk_id)
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s hasn't data with pk: %s!" % (node_id, pk_id))

    except:
        return HttpResponse("Get data filed!\n")

    return render_to_response("node_test.html", {'data': data})


@csrf_exempt
def loranodedata_add(request, gateway_id, node_id, data):
    try:
        gateway = Gateway.objects.get(gateway_id=gateway_id)
    except Gateway.DoesNotExist:
        return HttpResponse("gateway with ID %s doesn't exist!" % (gateway_id))

    try:
        loranode = LoRaNode.objects.get(node_id=node_id)
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s doesn't exist!" % (node_id))

    re_match = re.search(r'^data=(?P<data>\w+)', data)
    if re_match:
        rawdata = NodeRawData(data=re_match.group('data'), node=loranode, gateway=gateway)
        rawdata.save()

        servicedata = ServiceData(data1=rawdata.data, node=loranode, gateway=gateway)
        servicedata.save()

        if loranode.noderawdata_set.count() > 5:
            old_data = loranode.noderawdata_set.order_by('-time')[5:]
            for data in old_data:
                data.delete()

        if loranode.servicedata_set.count() > 5:
            old_data = loranode.servicedata_set.order_by('-time')[5:]
            for data in old_data:
                data.delete()

        return HttpResponse("Success!\n")

    else:
        return HttpResponse("POST data failed, format wrong!\n")


def map_uri(request):
	r = requests.session()
	url = "http://uri.amap.com/marker?position=116.473195,39.993253"
	result = r.get(url)
	content = result.content
	return HttpResponseRedirect(url)

#### REST API ###
class LoraNodeList(generics.ListCreateAPIView):
    queryset = LoRaNode.objects.all()
    serializer_class = LoraNodeSerializer


class LoraNodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoRaNode.objects.all()
    serializer_class = LoraNodeSerializer


#### RawData
class NodeRawDataList(generics.ListCreateAPIView):
    queryset = NodeRawData.objects.all()
    serializer_class = NodeRawDataSerializer


class NodeRawDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = NodeRawData.objects.all()
    serializer_class = NodeRawDataSerializer


###Service Data ###
class ServiceDataList(generics.ListCreateAPIView):
    queryset = ServiceData.objects.all()
    serializer_class = ServiceDataSerializer


class ServiceDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceData.objects.all()
    serializer_class = ServiceDataSerializer
