# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2019-02-20 02:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='icon',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]