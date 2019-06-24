from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.postgres.fields import ArrayField
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(validators=[validators.EmailValidator])
    phone = models.CharField(max_length=17, blank=True, validators=[RegexValidator(regex='^\d{10}$', message='Length has to be 10', code='Invalid number')])
    address_line_1 = models.CharField(
        "Address line 1",
        max_length=1024,
    )
    address_line_2 = models.CharField(
        "Address line 2",
        max_length=1024,
    )
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
    )

    def __str__(self):
        return self.name

class ProductOrder(models.Model):
    product_id = models.IntegerField()
    volume = models.CharField(max_length=10)
    quantity = models.IntegerField()
    flavour = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=200.00)
    def __str__(self):
        return self.name

class Order(models.Model):
    order_date = models.DateTimeField('date ordered', auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_order = models.ForeignKey(ProductOrder, on_delete=models.CASCADE)
    def __str__(self):
        return self.product_order.name

