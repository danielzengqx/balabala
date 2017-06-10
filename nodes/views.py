from django.shortcuts import render, HttpResponse, HttpResponseRedirect

# Create your views here.
def index(request):
	template = "index.html"
	context = {


	}
	return render(request, template, context)

import requests
def map_uri(request):
	r = requests.session()
	url = "http://uri.amap.com/marker?position=116.473195,39.993253"
	result = r.get(url)
	content = result.content
	return HttpResponseRedirect(url)


### REST Framework class based views ###
from nodes.models import Node
from nodes.serializers import NodeSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

class NodeList(generics.ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer


class NodeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializer    