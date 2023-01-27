from django.db import models
from product.models import Cart,Checkout,Products
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


class CheckoutSerializer(serializers.ModelSerializer):
    products = Productserializer(many=True)
    class Meta:
        model = Checkout
        fields ='__all__'