from django.http import HttpResponseNotFound
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.serialyzer import Productserializer, Cartserializer,CartSerializerTwo,OrderSerializer
from product.models import OrderProduct, Products,User,Order,Cart,Review
import json
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


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
    return Response(Productserializer(product).data)

####all the products
@api_view(['GET', 'POST'])
def api_list(request):
    """
    List of all the product, or create a new product.
    """
    if request.method == 'GET':
        products = Products.objects.all() ##Fetch the products
        serializer = Productserializer(products, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Productserializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
def delete_product(request,pk):
    try:
        product = Products.objects.get(pk=pk) #Get the porudct and Delete by ID
    except Products.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    request.method == 'DELETE'
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
def update_product(request,pk):
    try:
        product = Products.objects.get(pk=pk) #Get the porudct and Update by ID
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
    List of all the cart , or create a new cart.
    """
    user_name=request.query_params.get('username')
    if request.method == 'GET':
        print (user_name)
        user = User.objects.filter(username=user_name).first()
        if user:
            request.data['user'] = user.id
            print (user.id,'user')
            carts = Cart.objects.filter(user=user.id)
            print (carts.values())
            serializer = CartSerializerTwo(carts, many=True)
            return Response(serializer.data)
        
    elif request.method == 'POST':
        user_name = request.data.get('user')
        product_id = request.data.get('products')
        quantity = request.data.get('quantity')
        user = User.objects.filter(username=user_name).first()

        # Check if the user already has a cart for the given product
        cart = Cart.objects.filter(user=user, products=product_id).first()

        if cart:
            # Update the quantity of the existing cart
            cart.quantity += quantity
            cart.save()
            serializer = Cartserializer(cart)
            return Response(serializer.data)
        else:
            # Create a new cart instance
            if user:
                request.data['user'] = user.id
            serializer = Cartserializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

@api_view(['GET', 'POST'])
def single_cart(request,pk):
    try:
        cart=Cart.objects.get(pk=pk) #Get the cart by ID
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
        product = Cart.objects.filter(products_id=pk) #Get the cart by ID
    except Cart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    request.method == 'DELETE'
    product.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT'])
def update_cart(request,pk):
    print(request.data)
    try:
        product = Cart.objects.get(pk=pk) # Get the cart by ID
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
        user_id = request.data.get('cartlist')[0]['user'] # Get the User
        user = User.objects.filter(id=user_id).first() # Get the User from database
        order = Order.objects.create() # Create the order
        for cart in cartlist:
            product = cart['products']
            product = Products.objects.get(id=product.get('id')) # Get the product by ID
            quantity = cart['quantity']
            OrderProduct.objects.create(order=order, product=product, quantity=quantity, user=user)
        Cart.objects.filter(user=user_id).delete() # delete the cart after finished
        subject = 'Thanks for buying in our store'
        message = 'Dear {},\n\nThank you for your purchase!'.format(user.username)
        from_email = 'MoshikShopp@gmail.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        return Response({'success': True}, status=status.HTTP_201_CREATED)
    elif request.method == 'GET':
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    

@api_view(['POST'])
def prodectreview(request,pk):
    product = Products.objects.get(id=pk)
    user=request.user
    data=request.data
    review=Review.objects.create(
        user=user,
        product=product,
        name=user.first_name,
        rating=data['rating'],
        comment=data['comment'],
    )
    return Response({'detail':'Review added'})
    # #1 - Review already exists
    # alreadyexists=