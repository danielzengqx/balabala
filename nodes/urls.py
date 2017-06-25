from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.loranode_add, name='loranode_add'),
    url(r'^detail/(?P<node_id>\w+)/$', views.loranode_detail, name='loranode_detail'),
    url(r'^modify/(?P<node_id>\w+)/$', views.loranode_modify, name='loranode_modify'),
    url(r'^delete/(?P<node_id>\w+)/$', views.loranode_delete, name='loranode_delete'),
    url(r'^rawdata/(?P<node_id>\w+)/(?P<pk_id>\d+)/$', views.rawdata_detail, name='rawdata_detail'),
    url(r'^servicedata/(?P<node_id>\w+)/(?P<pk_id>\d+)/$', views.servicedata_detail, name='servicedata_detail'),

    url(r'^api/data/(?P<gateway_id>[0-9]+)/(?P<node_id>[0-9]+)/(?P<data>.*)/$', views.loranodedata_add, name='loranodedata_add'),
    #url(r'^map_uri/$',views.map_uri),
]

urlpatterns = format_suffix_patterns(urlpatterns)
