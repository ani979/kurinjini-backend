from django.shortcuts import render
from rest_framework import generics
from kbe.models import Customer, Order
from kbe.serializers import CustomerSerializer, OrderSerializer
from django.core.mail import EmailMessage, EmailMultiAlternatives
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

        def send_email(fromMail, toMail, order, products, phone):
            try:
                subject = "Your Kurinjini Order " + order + " has been received!"
                from_email = fromMail
                recipient_list = [toMail, "shilpi@kurinjiniskincare.com", "animesh@kurinjiniskincare.com"]
                html_content = '<h3 style="text-transform:uppercase;"> Dear ' + request.data['user']['fname'] + '</h3>' \
                                                                              '<br/>' \
                                '<p>Thank you for placing an order with us. ' \
                                    'We absolutely love that you gave us a chance to serve you. ' \
                                    'Your order details are as noted below:</p>'
                #print(phone)
                for aProduct in products:
                    #print(aProduct)
                    html_content = html_content + '<ul>Product:'
                    html_content = html_content + '<li> Name: ' + aProduct['name'] + '</li>'
                    html_content = html_content + '<li> Flavour: ' + aProduct['flavour'] + '</li>'
                    html_content = html_content + '<li> Volume/Weight: ' + aProduct['volume'] + '</li>'
                    html_content = html_content + '<li> Price: ' + str(aProduct['price']) + '</li>'
                    html_content = html_content + '<li> Quantity: ' + str(aProduct['quantity']) + '</li>'
                    html_content = html_content + '</ul>' + '<br\><br\>'

                html_content = html_content + '<p>' + 'We will get in touch with you shortly. </p>'
                #msg = EmailMultiAlternatives(subject, html_content, from_email, [recipient_list])
                email = EmailMultiAlternatives(subject, html_content, from_email, recipient_list)
                email.attach_alternative(html_content, "text/html")

                email.content_subtype = 'html'
                email.send()
            except KeyError:
                return print("error")
        # save customer
        customer = Customer.objects.filter(email=request.data['user']['email'])
        email = ''
        phone = ''
        if customer.exists():
            email = Customer.objects.values_list('email', flat=True).get(email=request.data['user']['email'])
            phone = Customer.objects.values_list('phone', flat=True).get(email=request.data['user']['email'])
        else:
            customer = {}
            customer['name'] = request.data['user']['fname'] + request.data['user']['lname']
            customer['phone'] = request.data['user']['phone']
            phone = customer['phone']
            customer['email'] = request.data['user']['email']
            email = customer['email']
            #print(customer)
            serializer = CustomerSerializer(data=customer)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)

        #print(email)
        # save product order
        products = []
        #print(request.data['items'])
        for po in request.data['items']:
            productOrder = {}
            productOrder['product_id'] = po['id']
            productOrder['volume'] = po['choosenSize']
            productOrder['quantity'] = po['qty']
            productOrder['flavour'] = po['flavour']
            productOrder['price'] = po['choosenPrice']
            productOrder['name'] = po['name']
            products.append(productOrder)
            #print(productOrder)
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
        print('phone' + phone)
        orderSerializer = OrderSerializer(data=order)
        if orderSerializer.is_valid():
            print(orderSerializer.validated_data)
            orderSerializer.save()
            send_email("orders@kurinjiniskincare.com",email,order['order_id'], products, phone)
            return Response(orderSerializer.data, status=status.HTTP_201_CREATED)

        return Response(orderSerializer.errors, status=status.HTTP_400_BAD_REQUEST)



