from rest_framework import serializers
from .models import Service





# class ServiceSerializer(serializers.Serializer):
#     service_id = serializers.CharField(max_length=64)
#     service_name = serializers.CharField(max_length=64)
#     max_nodes = serializers.IntegerField()
#     url = serializers.URLField(required=False)
#     description = serializers.CharField(max_length=3000)

#     def create(self, validated_data):
#         """
#         Create and return a new `Service` instance, given the validated data.
#         """
#         return Service.objects.create(**validated_data)

#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.service_name = validated_data.get('service_name', instance.service_name)
#         instance.max_nodes = validated_data.get('max_nodes', instance.max_nodes)
#         instance.url = validated_data.get('url', instance.url)
#         instance.description = validated_data.get('description', instance.description)
#         instance.save()
#         return instance


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('service_id', 'service_name', 'max_nodes', 'url', 'description')
