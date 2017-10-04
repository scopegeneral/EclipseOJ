# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 09:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='registered_user',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]