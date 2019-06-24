from django.contrib import admin
from .models import Customer, Order, ProductOrder

admin.site.register(Customer)
admin.site.register(ProductOrder)
admin.site.register(Order)


# Register your models here.
