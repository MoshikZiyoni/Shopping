import json
from django.http import HttpResponseNotFound, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.authentication import MyAuthentication
# from rest_framework.permissions import MyPermission
from product.serialyzer import Productserializer, Cartserializer
from product.models import Products
from product.models import Cart
from rest_framework.decorators import authentication_classes, permission_classes
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
        serializer = Cartserializer(carts, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print (request.data)
        serializer = Cartserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @authentication_classes([MyAuthentication])
# @permission_classes([MyPermission])
@api_view(['POST'])
def add_to_cart(request):
    product_id = request.data.get('product_id')
    print (product_id,'helooS')
    try:
        product = Products.objects.get(id=product_id)
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    quantity = request.data.get('quantity')
    # if request.user.is_authenticated:
    user = request.user
    # else:
    #     return Response(status=status.HTTP_401_UNAUTHORIZED)
    product = Products.objects.get(id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()
    return Response(status=status.HTTP_201_CREATED)



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
        product = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    request.method == 'DELETE'
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
def update_cart(request,pk):
    try:
        product = Cart.objects.get(pk=pk)
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    request.method == 'PUT'
    serializer = Cartserializer(product, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def my_view(request):
    products = Products.objects.all()
    return render(request, 'product_list.html', {'products': products})
