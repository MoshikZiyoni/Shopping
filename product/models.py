from django.db import models
from django.contrib.auth.models import User
# from rest_framework.authentication import MyAuthentication
# from rest_framework.permissions import MyPermission
from rest_framework import viewsets

# Create your models here.
class Products(models.Model):
    name=models.CharField(max_length=200)
    description=models.TextField(null=True)
    price=models.DecimalField(decimal_places=2,max_digits=10)
    created=models.DateField(auto_now_add=True)
    updated=models.DateField(auto_now=True)
    image=models.ImageField(null=True,blank=True,
                            default='/placeholder.jpg')


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    products = models.ForeignKey(Products, on_delete=models.CASCADE,unique=True)
    quantity=models.DecimalField(decimal_places=2,max_digits=10)

# class ProductViewSet(viewsets.ModelViewSet):
#     authentication_classes = (MyAuthentication,)
#     permission_classes = (MyPermission,)


class Checkout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    products = models.ManyToManyField(Products)
    quantity = models.DecimalField(decimal_places=2,max_digits=10)