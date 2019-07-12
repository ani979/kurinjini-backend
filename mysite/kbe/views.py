from django.shortcuts import render
from rest_framework import generics
from kbe.models import Customer, Order
from kbe.serializers import CustomerSerializer, OrderSerializer
from rest_framework.response import Response
from rest_framework import status
import json
import random
# Create your views here.
from django.http import HttpResponse


class CustomerListCreate(generics.ListCreateAPIView):
    queryset = Customer.objects.all()

    def post(self, request):

        def random_string():
            return str(random.randint(10000, 99999))
        # save customer
        customer = Customer.objects.filter(email=request.data['user']['email'])
        email = ''
        if customer.exists():
            email = Customer.objects.values_list('email', flat=True).get(email=request.data['user']['email'])
        else:
            customer = {}
            customer['name'] = request.data['user']['fname'] + request.data['user']['lname']
            customer['phone'] = request.data['user']['phone']
            customer['email'] = request.data['user']['email']
            email = customer['email']
            print(customer)
            serializer = CustomerSerializer(data=customer)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)

        print(email)
        # save product order
        products = []
        for po in request.data['items']:
            productOrder = {}
            productOrder['product_id'] = po['id']
            productOrder['volume'] = po['choosenSize']
            productOrder['quantity'] = po['qty']
            productOrder['flavour'] = po['name']
            productOrder['price'] = po['choosenPrice']
            productOrder['name'] = po['name']
            products.append(productOrder)
            print(productOrder)
            # poSerializer = ProductOrderSerializer(data=productOrder)
            # if poSerializer.is_valid():
            #     poSerializer.save()
            # else:
            #     return Response(poSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        order = {}
        order['customer'] = email
        order['price'] = request.data['total']
        order['products'] = {"products":len(products), "data":json.dumps(products)}
        print(order['products'])
        Order.objects.filter(order_id='').delete()
        key = ''
        while True:
            key = random_string()
            print(key)
            if not Order.objects.filter(order_id=key).exists():
                break
        order['order_id'] = 'KJN' + key
        print(order)
        orderSerializer = OrderSerializer(data=order)
        if orderSerializer.is_valid():
            print(orderSerializer.validated_data)
            orderSerializer.save()
            return Response(orderSerializer.data, status=status.HTTP_201_CREATED)

        return Response(orderSerializer.errors, status=status.HTTP_400_BAD_REQUEST)



