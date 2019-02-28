# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from djmoney.models.fields import MoneyField
import datetime
from django.utils.translation import gettext as _


# Create your models here.

class Cart(models.Model):
    id = models.AutoField(primary_key=True)
    orderid = models.CharField(max_length=250,null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    booking_ref = models.CharField(max_length=250, null=True,blank=True)
    user_id = models.IntegerField(blank=True, null=True, default=0)
    agent_ref = models.CharField(max_length=250,null=True, blank=True)
    notes = models.CharField(max_length=500,null=True, blank=True)
    status = models.IntegerField(blank=False, null=False, default=0)
    currency_id = models.IntegerField(blank=False, null=False, default=0)
    deliveryaddr1 = models.CharField(max_length=200, null=True, blank=True)
    deliveryaddr2 = models.CharField(max_length=200, null=True, blank=True)
    deliverycity = models.CharField(max_length=200, null=True, blank=True)
    deliverystate = models.CharField(max_length=100, null=True, blank=True)
    deliveryzip = models.CharField(max_length=20, null=True, blank=True)


class CartProducts(models.Model):
    id = models.AutoField(primary_key=True)
    cart = models.ForeignKey(
        'Cart',
        on_delete=models.CASCADE,
    )
    product_name = models.CharField(max_length=250,null=True, blank=True)
    fare = models.CharField(max_length=250,null=True, blank=True)
    validity = models.CharField(max_length=250, null=True, blank=True)
    service = models.CharField(max_length=250,null=True, blank=True)
    Rule = models.CharField(max_length=2000, null=True, blank=True)
    product_id = models.IntegerField(blank=False, null=False, default=0)
    start_date = models.DateField(blank=True, null=True)
    passengers_num = models.IntegerField(blank=False, null=False, default=0)
    adults_num = models.IntegerField(blank=False, null=False, default=0)
    non_adults_num = models.IntegerField(blank=False, null=False, default=0)    
    status = models.IntegerField(blank=False, null=False, default=0)
    settlementprice = models.FloatField(blank=False, default=0)
    netprice = models.FloatField(blank=False, default=0)
    grossprice = models.FloatField(blank=False, default=0)
    commissionprice = models.FloatField(blank=False, default=0)


class CartProductDetails(models.Model):
    id = models.AutoField(primary_key=True)
    cart_product = models.ForeignKey(
        'CartProducts',
        on_delete=models.CASCADE
    )
    from_station = models.CharField(max_length=250,null=True, blank=True)
    to_station = models.CharField(max_length=250,null=True, blank=True)
    from_code = models.CharField(max_length=20,null=True, blank=True)
    to_code = models.CharField(max_length=20,null=True, blank=True)
    departure_date = models.DateTimeField(blank=True, null=True)
    arrival_date = models.DateTimeField(blank=True, null=True)
    train = models.CharField(max_length=20, blank=True,null=True)
    train_category = models.CharField(max_length=50, blank=True,null=True)
    service = models.CharField(max_length=250, null=True, blank=True)


class CartProductPassengers(models.Model):
    id = models.AutoField(primary_key=True)
    cart_product = models.ForeignKey(
        'CartProducts',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=50, blank=True,null=True)
    first_name = models.CharField(max_length=250, blank=True,null=True)
    last_name = models.CharField(max_length=250, blank=True,null=True)
    age = models.IntegerField()
    dob = models.DateField(blank=True,null=True)
    nationality = models.CharField(max_length=20, blank=True,null=True)
    residencecountry = models.CharField(max_length=20, blank=True, null=True)
    passport = models.CharField(max_length=50, blank=True,null=True)