# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
