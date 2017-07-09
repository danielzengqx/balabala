from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.utils.timezone import localtime
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
from services.models import Service


def index(request):
    all_nodes = LoRaNode.objects.order_by('node_id')
    for loranode in all_nodes:
        try:
            rawdatas = loranode.noderawdata_set.all().order_by('-time')
        except:
            return HttpResponse("Get rawdata filed!\n")

        if rawdatas:
            if (datetime.now() - localtime(rawdatas[0].time).replace(tzinfo=None)).seconds > loranode.heartbeat_interval:
                loranode.device_status = 'inactive'
            else:
                loranode.device_status = 'active'
        else:
            if (datetime.now() - localtime(loranode.register_time).replace(tzinfo=None)).seconds > loranode.heartbeat_interval:
                loranode.device_status = 'inactive'
            else:
                loranode.device_status = 'active'
        loranode.save()
    return render_to_response("node_index.html", {'all_nodes': all_nodes})


def loranode_add(request):
    template = "node_add.html"
    if request.method == 'POST':
        #check the post value
        print(request.POST)
        form = LoRaNodeInfoForm(request.POST)
        if form.is_valid():
            loranode = form.save(commit=False)
            loranode.save()
            return HttpResponseRedirect('/nodes/')
        else:
            print("form is not valid!!")
            return render(request, template, {"form": form})
    else:
        form = LoRaNodeInfoForm()
        all_services = Service.objects.all()
        context = {
            'all_services': all_services,
            'form': form,
        }

    return render(request, template, context)


def loranode_detail(request, node_id):
    try:
        loranode = LoRaNode.objects.get(node_id=node_id)
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s doesn't exist!" % (node_id))

    try:
        rawdatas = loranode.noderawdata_set.all().order_by('-time')
    except:
        return HttpResponse("Get rawdata filed!\n")

    try:
        servicedatas = loranode.servicedata_set.all().order_by('-time')
    except:
        return HttpResponse("Get data filed!\n")

    if rawdatas:
        if (datetime.now() - localtime(rawdatas[0].time).replace(tzinfo=None)).seconds > loranode.heartbeat_interval:
            loranode.device_status = 'inactive'
        else:
            loranode.device_status = 'active'
    else:
        if (datetime.now() - localtime(loranode.register_time).replace(tzinfo=None)).seconds > loranode.heartbeat_interval:
            loranode.device_status = 'inactive'
        else:
            loranode.device_status = 'active'
    loranode.save()
    loranodedata_update(node_id)
    return render_to_response("node_test.html", {'loranode': loranode, 'rawdatas': rawdatas, 'servicedatas': servicedatas})


def loranode_modify(request, node_id):
    try:
        loranode = LoRaNode.objects.get(node_id=node_id)
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s doesn't exist!" % (node_id))

    template = "node_test.html"
    if request.method == 'POST':
        form = LoRaNodeInfoForm(request.POST)
        if form.is_valid():
            loranode = form.save(commit=False)
            loranode.save()
            return HttpResponseRedirect('/nodes/')
        else:
            print("form is not valid!!")
            return render(request, template, {"form": form})
    else:
        form = LoRaNodeInfoForm()

    return render_to_response(template, {'form': form})


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


def loranodedata_update(node_id):
    try:
        loranode = LoRaNode.objects.get(node_id=node_id)
    except LoRaNode.DoesNotExist:
        print("loranode with ID %s doesn't exist!\n" % (node_id))
        return 0

        '''
        rawdata = NodeRawData(data=re_match.group('data'), node=loranode, gateway=gateway)
        rawdata.save()

        servicedata = ServiceData(data1=rawdata.data, node=loranode, gateway=gateway)
        servicedata.save()'''

    old_data = loranode.noderawdata_set.order_by('-time')[loranode.max_data_record:]
    for data in old_data:
        try:
            data.delete()
        except:
            print("delete date fail!\n")

    old_data = loranode.servicedata_set.order_by('-time')[loranode.max_data_record:]
    for data in old_data:
        try:
            data.delete()
        except:
            print("delete date fail!\n")

    return 1


def map_uri(request):
	r = requests.session()
	url = "http://uri.amap.com/marker?position=116.473195,39.993253"
	result = r.get(url)
	content = result.content
	return HttpResponseRedirect(url)


####REST API
class LoraNodeList(generics.ListCreateAPIView):
    queryset = LoRaNode.objects.all()
    serializer_class = LoraNodeSerializer


class LoraNodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = LoRaNode.objects.all()
    serializer_class = LoraNodeSerializer


####RawData
class NodeRawDataList(generics.ListCreateAPIView):
    queryset = NodeRawData.objects.all()
    serializer_class = NodeRawDataSerializer


class NodeRawDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = NodeRawData.objects.all()
    serializer_class = NodeRawDataSerializer


###Service Data
class ServiceDataList(generics.ListCreateAPIView):
    queryset = ServiceData.objects.all()
    serializer_class = ServiceDataSerializer


class ServiceDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ServiceData.objects.all()
    serializer_class = ServiceDataSerializer
