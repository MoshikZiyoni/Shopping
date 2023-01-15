from django.db import models
from product.models import Products
from rest_framework.serializers import ModelSerializer
from product.models import Cart
from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

class Productserializer(ModelSerializer):
    # get_image = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = '__all__'
    
    def get_image(self, obj):
        return self.context['request'].build_absolute_uri(obj.image.url)
    # def get_image(self, obj):
    #     return obj.image.url       

class Cartserializer(ModelSerializer):
    class Meta:
        model= Cart
        fields = '__all__'
        