from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$',views.index, name='index'),
    url(r'^list/$', views.NodeList.as_view()),
    url(r'^detail/(?P<pk>[0-9]+)/$', views.NodeDetail.as_view()),
    url(r'^map_uri/$',views.map_uri),

]

urlpatterns = format_suffix_patterns(urlpatterns)
