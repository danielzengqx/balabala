from django.contrib import admin
from nodes.models import *
# Register your models here.
class NodeAdmin(admin.ModelAdmin):
    list_display = ('id', 'created',)


admin.site.register(Node, NodeAdmin)