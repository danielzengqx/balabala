from django.conf.urls import url
from django.contrib import admin
from . import views

### REST API ###
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^add/$', views.service_add, name='service_add'),
    url(r'^detail/(?P<service_id>\w+)/$', views.service_detail, name='service_detail'),
    url(r'^modify/(?P<service_id>\w+)/$', views.service_modify, name='service_modify'),
    url(r'^delete/(?P<service_id>\w+)/$', views.service_delete, name='service_delete'),

	### REST API ###
	url(r'^api/$', views.ServiceList.as_view()),
    url(r'^api/(?P<pk>[0-9]+)/$', views.ServiceDetail.as_view()),


]


### REST API ###
urlpatterns = format_suffix_patterns(urlpatterns)
