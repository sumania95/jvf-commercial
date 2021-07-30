from django.db import models
from django.db.models import Model, ForeignKey
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import datetime
from django.utils import timezone
import uuid

loc_category = (
    ('1', 'Office',),
    ('2', 'Van',),
)


class Branch(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    branch                  = models.CharField(max_length = 200)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.branch)

    class Meta:
        ordering = ['branch']

category = (
    ('1', 'Private',),
    ('2', 'Government',),
)

class Customer(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name                    = models.CharField(max_length = 200)
    address                 = models.CharField(max_length = 200)
    category                = models.CharField(choices=category,max_length = 200)
    branch                  = models.ForeignKey(Branch, on_delete = models.CASCADE)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name']

condition = (
    ('1', 'Brand New Unit',),
    ('2', 'Unit Operational',),
    ('3', 'Unit Standby',),
    ('4', 'Unit Repair',),
    ('5', 'Under Observation',),
)

class Transaction(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer                = models.ForeignKey(Customer, on_delete = models.CASCADE)
    brand                   = models.CharField(max_length = 200)
    model                   = models.CharField(max_length = 200)
    type                    = models.CharField(max_length = 200)
    khr                     = models.CharField(max_length = 200)
    engine_no               = models.CharField(max_length = 200)
    chassis_no              = models.CharField(max_length = 200)
    description             = models.CharField(max_length = 200)
    condition               = models.CharField(choices=condition,max_length = 200)
    date                    = models.DateField(default=timezone.now)
    technician              = models.CharField(max_length = 200)
    branch                  = models.ForeignKey(Branch, on_delete = models.CASCADE)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.name)

class User_Type(models.Model):
    branch                  = models.ForeignKey(Branch, on_delete = models.CASCADE)
    user                    = models.OneToOneField(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.branch)

class Brand(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand                   = models.CharField(max_length = 200)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.brand)

    class Meta:
        ordering = ['brand']


currency = (
    ('1', 'JPY',),
    ('2', 'USD',),
    ('3', 'PHP',),
    ('4', 'EUR',),
)

class Product(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    part_number             = models.CharField(max_length = 200,blank=True)
    description             = models.CharField(max_length = 200)
    brand                   = models.ForeignKey(Brand, on_delete = models.CASCADE)
    location                = models.CharField(max_length = 200)
    currency                = models.CharField(default="1",choices=currency,max_length = 200)
    quantity                = models.IntegerField(default=0)
    unit_price              = models.DecimalField(default=0,max_digits = 50,decimal_places=2)
    branch                  = models.ForeignKey(Branch, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.description + " - " + self.part_number)

    class Meta:
        ordering = ['description','part_number']

class Receiving(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    control_no              = models.CharField(default="0000",max_length = 200)
    vendor                  = models.CharField(max_length = 200)
    shipped_via             = models.CharField(blank=True,max_length = 200)
    invoice_no              = models.CharField(max_length = 200)
    remarks                 = models.CharField(blank=True,max_length = 200)
    branch                  = models.ForeignKey(Branch, on_delete = models.CASCADE)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

class Receiving_Detail(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    receiving               = models.ForeignKey(Receiving, on_delete = models.CASCADE)
    product                 = models.ForeignKey(Product, on_delete = models.CASCADE)
    condition               = models.CharField(blank=True,max_length = 200)
    quantity                = models.IntegerField(default=1)

    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

category = (
    ('1', 'Sales',),
    ('2', 'Warranty',),
    ('3', 'Transfer',),
)

class Releasing(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    control_no              = models.CharField(default="0000",max_length = 200)
    category                = models.CharField(choices=category,max_length = 200)
    customer_name           = models.CharField(max_length = 200)
    purchase_order_number   = models.CharField(blank=True,max_length = 200)
    others                  = models.CharField(blank=True,max_length = 200)
    branch                  = models.ForeignKey(Branch, on_delete = models.CASCADE)
    user                    = models.ForeignKey(User, on_delete = models.CASCADE)
    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)

class Releasing_Detail(models.Model):
    id                      = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    releasing               = models.ForeignKey(Releasing, on_delete = models.CASCADE)
    product                 = models.ForeignKey(Product, on_delete = models.CASCADE)
    quantity                = models.IntegerField(default=1)

    date_updated            = models.DateTimeField(auto_now = True)
    date_created            = models.DateTimeField(auto_now_add = True)
