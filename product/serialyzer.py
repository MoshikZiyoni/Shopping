from django.db import models
from product.models import Products
from rest_framework.serializers import ModelSerializer
from product.models import Cart
from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

class Productserializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Products
        fields = '__all__'
    
    # def get_image(self, obj):
    #     return self.context['request'].build_absolute_uri(obj.image.url)
        
# def get_product_details(self, obj):
#     product = Products.objects.get(pk=obj.products.pk)
#     serializer = Productserializer(product)
#     return serializer.data


class Cartserializer(serializers.ModelSerializer):
    
    # products = Productserializer()
    class Meta:
        model= Cart
        # fields = '__all__'
        fields = ( 'products','quantity','user' )
        
    
class CartSerializerTwo(serializers.ModelSerializer):
    products = Productserializer()
    class Meta:
        model= Cart
        # fields = '__all__'
        fields = ( 'products','quantity','user' )