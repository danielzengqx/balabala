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
        rawdatas = ''
        try:
            rawdatas = loranode.noderawdata_set.all().order_by('-time')
        except:
            print("Get rawdata filed!\n")

        if rawdatas:
            if (datetime.now() > localtime(rawdatas[0].time).replace(tzinfo=None)
                and (datetime.now() - localtime(rawdatas[0].time).replace(tzinfo=None)).seconds > loranode.heartbeat_interval):
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

    loranodedata_update(node_id)
    rawdatas = ''
    try:
        rawdatas = loranode.noderawdata_set.all().order_by('-time')
    except:
        print("Get rawdata filed!\n")

    servicedatas = ''
    try:
        servicedatas = loranode.servicedata_set.all().order_by('-time')
    except:
        print("Get data filed!\n")

    if rawdatas:
        if (datetime.now() > localtime(rawdatas[0].time).replace(tzinfo=None)
            and (datetime.now() - localtime(rawdatas[0].time).replace(tzinfo=None)).seconds > loranode.heartbeat_interval):
            loranode.device_status = 'inactive'
        else:
            loranode.device_status = 'active'
    else:
        if (datetime.now() - localtime(loranode.register_time).replace(tzinfo=None)).seconds > loranode.heartbeat_interval:
            loranode.device_status = 'inactive'
        else:
            loranode.device_status = 'active'
    loranode.save()
    return render_to_response("node_detail.html", {'loranode': loranode, 'rawdatas': rawdatas, 'servicedatas': servicedatas})


def loranode_modify(request, node_id):
    all_services = Service.objects.all()
    try:
        loranode = LoRaNode.objects.get(node_id=node_id)
    except LoRaNode.DoesNotExist:
        return HttpResponse("loranode with ID %s doesn't exist!" % (node_id))

    template = "node_modify.html"
    if request.method == 'POST':
        print(request.POST)
        form = LoRaNodeInfoForm(request.POST, instance=loranode)
        if form.is_valid():
            print('form is valid!')
            loranode = form.save(commit=False)
            loranode.save()

            return HttpResponseRedirect('/nodes/')
        else:
            print("form is not valid!!")
            return render(request, template, {"form": form})
    else:
        form = LoRaNodeInfoForm()
        context = {
            "loranode": loranode,
            "all_services": all_services,
            "form": form,
        }
    return render(request, template, context)


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

    def post(self, request, *args, **kwargs):
        servicedata_create(types='carport', **request.POST)
        return self.create(request, *args, **kwargs)

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


def servicedata_create(types='carport', **info):
    print(types, info, '\n')
    if types in ['carport', 'common_types']:
        try:
            loranode = LoRaNode.objects.get(node_id=info['node'][0])
        except LoRaNode.DoesNotExist:
            print("loranode with ID %s doesn't exist!" % (info['node'][0]))
            return

        try:
            gateway = Gateway.objects.get(gateway_id=info['gateway'][0])
        except Gateway.DoesNotExist:
            print("gateway with ID %s doesn't exist!" % (info['gateway'][0]))
            return

        print(re.split(r'#', info['data'][0]), '\n')
        servicedata = {
            'info1': '',
            'info2': '',
            'info3': '',
            'data1': '',
            'data2': '',
            'data3': '',
        }
        (servicedata['info1'], servicedata['data1'], servicedata['info2'], servicedata['data2'], servicedata['info3'], servicedata['data3'], *unuse) = re.split(r'#', info['data'][0] + '######')
        service_data = ServiceData(**servicedata, node=loranode, gateway=gateway).save()

    elif types in ['type1', ]:
        pass

    elif types in ['type2', ]:
        pass

    else:
        print("service data create fail, unknow service type: %s!\n" % (types))

        return 0


def listnodes():
    all_nodes = LoRaNode.objects.order_by('node_id')
    for loranode in all_nodes:
        print(loranode.node_id, '==', loranode.node_name, sep=' ')


def create_rawdata(timestart, timeend, timestep, nodeid, gatewayid):
    import calendar
    import pytz
    try:
        loranode = LoRaNode.objects.get(node_id=nodeid)
    except LoRaNode.DoesNotExist:
        print("loranode with ID %s doesn't exist!" % (nodeid))
        return

    try:
        gateway = Gateway.objects.get(gateway_id=gatewayid)
    except Gateway.DoesNotExist:
        print("gateway with ID %s doesn't exist!" % (gatewayid))
        return



    m_timestart = re.match(r'^(?P<year>\d{4})\-(?P<mon>\d{1,2})\-(?P<day>\d{1,2})$', str(timestart))
    m_timeend = re.match(r'^(?P<year>\d{4})\-(?P<mon>\d{1,2})\-(?P<day>\d{1,2})$', str(timeend))
    m_timestep = re.match(r'^(?P<step>\d+)(?P<unit>mon|day|hour)$', str(timestep))

    if m_timestart and m_timeend and m_timestep and (int(m_timeend.group('year')) > int(m_timestart.group('year')) or
        (int(m_timeend.group('year')) == int(m_timestart.group('year')) and int(m_timeend.group('mon')) > int(m_timestart.group('mon'))) or
        (int(m_timeend.group('year')) == int(m_timestart.group('year')) and int(m_timeend.group('mon')) == int(m_timestart.group('mon')) and int(m_timeend.group('day')) > int(m_timestart.group('day')))):
        pass

    else:
        print('Args check failed: timestart=%s timeend=%s timestep=%s\n' % (timestart, timeend, timestep,))
        return

    times = []
    if m_timestep.group('unit') == 'mon':
        year = int(m_timestart.group('year'))
        mon = int(m_timestart.group('mon')) - int(m_timestep.group('step'))
        for i in range(0, (int(m_timeend.group('year')) - int(m_timestart.group('year'))) * 12 + int(m_timeend.group('mon')) - int(m_timestart.group('mon')) + 1, int(m_timestep.group('step'))):
            mon += int(m_timestep.group('step'))

            if mon > 12:
                mon -= 12
                year = int(m_timestart.group('year')) + 1
            times.append((year, mon, 1, 12, 1, 1))
            print((year, mon, 1, 12, 1, 1))

    elif m_timestep.group('unit') == 'day':
        year = int(m_timestart.group('year'))
        mon = int(m_timestart.group('mon')) - 1
        day_init = int(m_timestart.group('day'))
        for i in range(0, (int(m_timeend.group('year')) - int(m_timestart.group('year'))) * 12 + int(m_timeend.group('mon')) - int(m_timestart.group('mon')) + 1):
            mon += 1

            if mon > 12:
                mon -= 12
                year = int(m_timestart.group('year')) + 1

            if i == (int(m_timeend.group('year')) - int(m_timestart.group('year'))) * 12 + int(m_timeend.group('mon')) - int(m_timestart.group('mon')):
                for day in range(1, int(m_timeend.group('day')) + 1, int(m_timestep.group('step'))):
                    times.append((year, mon, day, 12, 1, 1))
                    print((year, mon, day, 12, 1, 1))
            elif i == 0:
                days = calendar.monthrange(year, mon)
                for day in range(day_init, days[1] + 1, int(m_timestep.group('step'))):
                    times.append((year, mon, day, 12, 1, 1))
                    print((year, mon, day, 12, 1, 1))
            else:
                days = calendar.monthrange(year, mon)
                for day in range(1, days[1] + 1, int(m_timestep.group('step'))):
                    times.append((year, mon, day, 12, 1, 1))
                    print((year, mon, day, 12, 1, 1))

    elif m_timestep.group('unit') == 'hour':
        year = int(m_timestart.group('year'))
        mon = int(m_timestart.group('mon')) - 1
        day_init = int(m_timestart.group('day'))
        for i in range(0, (int(m_timeend.group('year')) - int(m_timestart.group('year'))) * 12 + int(m_timeend.group('mon')) - int(m_timestart.group('mon')) + 1):
            mon += 1

            if mon > 12:
                mon -= 12
                year = int(m_timestart.group('year')) + 1

            if i == (int(m_timeend.group('year')) - int(m_timestart.group('year'))) * 12 + int(m_timeend.group('mon')) - int(m_timestart.group('mon')):
                for day in range(1, int(m_timeend.group('day')) + 1):
                    for hour in range(0, 24, int(m_timestep.group('step'))):
                        times.append((year, mon, day, hour, 1, 1))
                        print((year, mon, day, hour, 1, 1))
            elif i == 0:
                days = calendar.monthrange(year, mon)
                for day in range(day_init, days[1] + 1):
                    for hour in range(0, 24, int(m_timestep.group('step'))):
                        times.append((year, mon, day, hour, 1, 1))
                        print((year, mon, day, hour, 1, 1))
            else:
                days = calendar.monthrange(year, mon)
                for day in range(1, days[1] + 1):
                    for hour in range(0, 24, int(m_timestep.group('step'))):
                        times.append((year, mon, day, hour, 1, 1))
                        print((year, mon, day, hour, 1, 1))

    else:
        pass

    for one_time in times:
        rawdata = NodeRawData(data='just for test', node=loranode, gateway=gateway)
        rawdata.time = datetime(*one_time, tzinfo=pytz.timezone('UTC'))
        rawdata.save()
