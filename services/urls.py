from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^add/$', views.service_add, name='service_add'),
    url(r'^detail/$', views.service_detail, name='service_detail'),
]