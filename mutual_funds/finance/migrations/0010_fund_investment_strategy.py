# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-06 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0009_auto_20161128_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='fund',
            name='investment_strategy',
            field=models.TextField(blank=True, null=True),
        ),
    ]
