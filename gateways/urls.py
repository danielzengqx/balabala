from django.conf.urls import url
from django.contrib import admin
from . import views

### REST API ###
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^add/$', views.gateway_add, name='gateway_add'),
    url(r'^detail/(?P<gateway_id>\w+)', views.gateway_detail, name='gateway_detail'),
    url(r'^modify/(?P<gateway_id>\w+)', views.gateway_modify, name='gateway_modify'),
    url(r'^delete/(?P<gateway_id>\w+)', views.gateway_delete, name='gateway_delete'),

	url(r'^api/$', views.GatewayList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views.GatewayDetail.as_view()),
]


### REST API ###
urlpatterns = format_suffix_patterns(urlpatterns)
