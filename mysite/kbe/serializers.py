from rest_framework import serializers
from kbe.models import Customer, Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    customer = serializers.SlugRelatedField(
        slug_field='email',
        queryset=Customer.objects.all()
    )
    class Meta:
        model = Order
        fields = '__all__'