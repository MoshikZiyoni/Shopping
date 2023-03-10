from django.db import models
from product.models import Cart,Products,Order,OrderProduct
from rest_framework import serializers

class Productserializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Products
        fields = '__all__'
    


class Cartserializer(serializers.ModelSerializer):
    
    class Meta:
        model= Cart
        # fields = ( 'products','quantity','user' )
        fields = '__all__'

        
    
class CartSerializerTwo(serializers.ModelSerializer):
    products = Productserializer()
    class Meta:
        model= Cart
        fields = '__all__'



class OrderSerializer(serializers.ModelSerializer):
    products = models.ManyToManyField(Products)
    class Meta:
        model = Order
        fields = '__all__'


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderProduct
        fields = '__all__'

