# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-21 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0002_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='acceptedA',
            field=models.IntegerField(default=0),
        ),
    ]