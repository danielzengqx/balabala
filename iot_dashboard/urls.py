"""iot_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from . import views
from django.contrib.auth import views as auth_views

# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^$',views.index),
    url(r'^admin/', admin.site.urls),

    # url(r'^login$', auth_views.LoginView.as_view),
    url(r'^accounts/login/$', auth_views.LoginView.as_view(), name="login"),
    url(r'^accounts/logout/$', auth_views.LogoutView.as_view(template_name="registration/login.html")),
    url(r'^accounts/signup/$', views.signup),
    url(r'^accounts/profile/$', views.index),  ## for temporary  use

    ### Password Reset ###
    url(r'^accounts/passwd_reset/$', auth_views.PasswordResetView.as_view(template_name="registration/passwd_reset.html"), name="password_reset"),
    url(r'^accounts/passwd_reset_done/$', auth_views.PasswordResetDoneView.as_view(template_name="registration/passwd_reset_done.html"), name="password_reset_done"),    
    url(r'^accounts/passwd_reset_confirm/uidb64=(?P<uidb64>\S+)/token=(?P<token>\S+)$', auth_views.PasswordResetConfirmView.as_view(template_name="registration/passwd_reset_confirm.html"), name="password_reset_confirm"),
    url(r'^accounts/passwd_reset_complete/$', auth_views.PasswordResetCompleteView.as_view(template_name="registration/passwd_reset_complete.html"), name="password_reset_complete"),    

    ###REST Framework
    url(r'^api', include(router.urls)),  
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),  

    url(r'^nodes/', include('nodes.urls')),
    url(r'^gateways/', include('gateways.urls')),
    url(r'^services/', include('services.urls')),

]
