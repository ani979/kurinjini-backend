from django.db import models
from django.contrib.postgres.fields import JSONField
from django.core import validators
from django.core.validators import RegexValidator

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(validators=[validators.EmailValidator],primary_key=True)
    phone = models.CharField(max_length=17, blank=True)
    address_line_1 = models.CharField(
        "Address line 1",
        max_length=1024,
        blank=True
    )
    address_line_2 = models.CharField(
        "Address line 2",
        max_length=1024,
        blank=True
    )
    address = models.TextField("", null=True, blank=True)
    city = models.CharField(max_length=100, blank = True)
    state = models.CharField(max_length=100, blank = True)
    country = models.CharField(max_length=100, blank = True)
    zip_code = models.CharField(
        "ZIP / Postal code",
        max_length=12,
        blank = True
    )

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.CharField(primary_key=True, max_length=9)
    order_date = models.DateTimeField('date ordered', auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = JSONField()
    price = models.DecimalField(max_digits=6, decimal_places=2, default=200.00)
    notes = models.TextField("", null=True, blank=True)

    def __str__(self):
        return self.order_id


