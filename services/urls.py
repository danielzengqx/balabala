from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^add/$', views.service_add, name='service_add'),
    url(r'^detail/(?P<service_id>\w+)', views.service_detail, name='service_detail'),
    url(r'^modify/(?P<service_id>\w+)', views.service_modify, name='service_modify'),
]