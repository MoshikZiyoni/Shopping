from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.authentication import MyAuthentication
# from rest_framework.permissions import MyPermission
from product.serialyzer import Productserializer, Cartserializer,CartSerializerTwo,OrderSerializer
from product.models import OrderProduct, Products,User,Order,Cart
from rest_framework.decorators import authentication_classes, permission_classes
import json


@api_view(['GET', 'POST'])
def single_product(request,pk):
    try:
        product=Products.objects.get(pk=pk)
    except Products.DoesNotExist:
        # Whoopsie
        return HttpResponseNotFound(
            json.dumps({"ERR": f"car  with id {id} not found"}),
            content_type="application/json",
        )

    # Serialise your car or do something with it
    return Response(Productserializer(product).data)


@api_view(['GET', 'POST'])
def api_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        products = Products.objects.all()
        serializer = Productserializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Productserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'DELETE'])

def delete_product(request,pk):
    try:
        product = Products.objects.get(pk=pk)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    request.method == 'DELETE'
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
def update_product(request,pk):
    try:
        product = Products.objects.get(pk=pk)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    request.method == 'PUT'
    serializer = Productserializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def cart_list(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'GET':
        carts = Cart.objects.all()
        serializer = CartSerializerTwo(carts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST': 
        serializer = Cartserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def single_cart(request,pk):
    try:
        cart=Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        # Whoopsie
        return HttpResponseNotFound(
            json.dumps({"ERR": f"car  with id {id} not found"}),
            content_type="application/json",
        )

    # Serialise your car or do something with it
    return Response(Cartserializer(cart).data)

@api_view(['GET', 'DELETE'])
def delete_cart(request,pk):
    try:
        product = Cart.objects.filter(products_id=pk)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    request.method == 'DELETE'
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
def update_cart(request,pk):
    print(request.data)
    try:
        product = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    request.method == 'PUT'
    serializer = Cartserializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        print ('Update Success')
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def my_view(request):
    products = Products.objects.all()
    return render(request, 'product_list.html', {'products': products})


@api_view(['POST', 'GET'])
def save_checkout_data(request):
    if request.method == 'POST':
        cartlist = request.data.get('cartlist')
        print (cartlist,'cartlist')
        user_id = request.data.get('cartlist')[0]['user']
        print(user_id,'userrrrrrr')
        order = Order.objects.create() # Create the order
        for cart in cartlist:
            product = cart['products']
            print (product.get('id'))
            product = Products.objects.get(id=product.get('id'))
            quantity = cart['quantity']
            OrderProduct.objects.create(order=order, product=product, quantity=quantity)
        Cart.objects.filter(user=user_id).delete() # delete the cart

        return Response({'success': True}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
