# -*- coding: utf-8 -*-
# Generated by Django 1.9.11 on 2016-12-06 18:06
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_remove_managementcompany_fund_manager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='managementcompany',
            name='investment_strategy',
        ),
    ]
