# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-18 18:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0004_auto_20190214_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproducts',
            name='adults_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cartproducts',
            name='non_adults_num',
            field=models.IntegerField(default=0),
        ),
    ]
