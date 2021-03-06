from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from .form import ServiceInfoForm
from .models import Service
from nodes.models import LoRaNode
from django.conf import settings
import os
from datetime import datetime
import calendar
import pytz
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
            loranodes = service.loranode_set.all().order_by('-register_time')
        except Exception as e:
            print("Get loranodes filed!\n", e)

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

    time_now = datetime.now()
    mon = time_now.month
    year = time_now.year
    times = []
    for i in range(12):
        if mon > i:
            times.append((year, mon - i))
        else:
            times.append((year - 1, mon + 12 - i))

    nodes_info = {}
    for year, mon in times:
        days = calendar.monthrange(year, mon)
        nodes = LoRaNode.objects.filter(service=service_id).filter(register_time__lte=datetime(year, mon, days[1], tzinfo=pytz.timezone('UTC')))
        register_nodes = nodes.count()
        active_nodes = 0
        for node in nodes:
            rawdatas = ''
            try:
                rawdatas = node.noderawdata_set.filter(time__gte=datetime(year, mon, 1, tzinfo=pytz.timezone('UTC'))).filter(time__lt=datetime(year, mon, days[1], tzinfo=pytz.timezone('UTC')))
            except:
                print("Get rawdata filed!\n")

            if rawdatas:
                active_nodes += 1

        nodes_info['{}-{}'.format(year, mon)] = {
            'register_nodes': register_nodes,
            'active_nodes': active_nodes,
        }
        #print(nodes_info)



    time_axis = list()
    for i in calendar.month_name[1:]:
        print("i ", i)
        time_axis.append(str(i))
        if i == time_now.strftime("%B"):
            break


    print(time_axis)
    
    # time_axis, data_num = getDataNum(service_id, time_now.year() + "-01", time_now.strftime("%Y-%m-%d"))


    template = "service_detail.html"
    context = {
        "single_service": single_service,
        "service_nodes": loranodes,
        "nodes_info": nodes_info,
        "time_axis": time_axis
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

# Create your views here.
def map(request):
    all_nodes = LoRaNode.objects.all()
    for node in all_nodes:
        print(node)

    print(settings.MEDIA_ROOT)

    path = "10w.txt"
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    with open(file_path, "w") as f:
            for node in all_nodes:
                f.write(str(node.longitude))
                f.write(", ")
                f.write(str(node.latitude))


                f.write("\n")

    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            # response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            # response['Content-Disposition'] = 'content; filename=' + os.path.basename(file_path)
            # return response
            # f = open(file_path)
            content = fh.read()
            return HttpResponse(content, content_type='text/plain;charset=utf-8')


def listservices():
    services = Service.objects.all()
    for service in services:
        print(service.service_id, '==', service.service_name, sep=' ')


def service_data(service_id, date_start, date_end):
    s_year, s_mon = date_start.split('-')
    e_year, e_mon = date_end.split('-')
    s_year, s_mon, e_year, e_mon = [int(item) for item in [s_year, s_mon, e_year, e_mon]]
    if (s_year < e_year) or (s_year == e_year and s_mon <= e_mon):
        pass
    else:
        print("Arg wrong!\n")
        return

    single_service = Service.objects.get(service_id=service_id)
    service_data = {}
    service_data[single_service.service_id] = {}

    while(True):

        days = calendar.monthrange(s_year, s_mon)
        nodes = LoRaNode.objects.filter(service=single_service.service_id).filter(register_time__lte=datetime(s_year, s_mon, days[1], tzinfo=pytz.timezone('UTC')))
        data_num = 0
        for node in nodes:
            try:
                rawdatas = node.noderawdata_set.filter(time__gte=datetime(s_year, s_mon, 1, tzinfo=pytz.timezone('UTC'))).filter(time__lt=datetime(s_year, s_mon, days[1], tzinfo=pytz.timezone('UTC')))
                data_num += rawdatas.count()
            except:
                print("Get rawdata filed!\n")


        service_data[single_service.service_id]['{}/{}'.format(s_year, s_mon)] = {
            'data_num': data_num,
        }
        print(single_service.service_id, s_year, s_mon, service_data[single_service.service_id]['{}/{}'.format(s_year, s_mon)], '\n')

        if s_year == e_year and s_mon == e_mon:
            break

        s_mon += 1
        if s_mon > 12:
            s_mon = 1
            s_year += 1

    return service_data

def getDataNum(request, service_id, date_start=str(datetime.now().year) + "-01", date_end=datetime.today().strftime("%Y-%m")):
    data = service_data(service_id, date_start, date_end)
    print(data)
    time_axis = list()
    import  json
    a = [v["data_num"] for k,v  in data[service_id].items()]
    print(a)

    result = json.dumps({
        # "timeAxis":[10,20,30,40],
        "timeAxis": list(data[service_id].keys()),
        # "dataNum":[10,20,30,40]
        "dataNum": a
        })

    print(result)
    return HttpResponse(result, content_type='application/json')


#### REST API ###
class ServiceList(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
