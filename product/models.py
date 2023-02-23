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
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True)
    products = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity=models.SmallIntegerField()



class Order(models.Model):
    products = models.ManyToManyField(Products)
    order_date=models.DateField(auto_now_add=True)
    quantity=models.SmallIntegerField(null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True)

class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity=models.SmallIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True)

class Review(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE ,null=True)
    comment=models.TextField(max_length=250,blank=True)
    rate=models.IntegerField(default=0)
    created_date=models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.rate)