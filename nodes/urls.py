from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.loranode_add, name='loranode_add'),
    url(r'^detail/(?P<node_id>\w+)/$', views.loranode_detail, name='loranode_detail'),
    url(r'^modify/(?P<node_id>\w+)/$', views.loranode_modify, name='loranode_modify'),
    url(r'^delete/(?P<node_id>\w+)/$', views.loranode_delete, name='loranode_delete'),
    url(r'^rawdata/(?P<node_id>\w+)/$', views.rawdata_list, name='rawdata_list'),
    url(r'^rawdata/(?P<node_id>\w+)/(?P<pk_id>\d+)/$', views.rawdata_detail, name='rawdata_detail'),
    url(r'^servicedata/(?P<node_id>\w+)/$', views.servicedata_list, name='servicedata_list'),
    url(r'^servicedata/(?P<node_id>\w+)/(?P<pk_id>\d+)/$', views.servicedata_detail, name='servicedata_detail'),
    #url(r'^map_uri/$',views.map_uri),

    ### REST API ###
    ## LoraNode ##
	url(r'^api/LoraNode/$', views.LoraNodeList.as_view()),
    url(r'^api/LoraNode/(?P<pk>[0-9]+)/$', views.LoraNodeDetail.as_view()),

    ## RawData ##
	url(r'^api/NodeRawData/$', views.NodeRawDataList.as_view()),
    url(r'^api/NodeRawData/(?P<pk>[0-9]+)/$', views.NodeRawDataDetail.as_view()),

    ## ServiceData ##
	url(r'^api/ServiceData/$', views.ServiceDataList.as_view()),
    url(r'^api/ServiceData/(?P<pk>[0-9]+)/$', views.ServiceDataDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
