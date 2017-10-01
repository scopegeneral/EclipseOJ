from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    country = CountryField(default='IN')
    institute = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    rating = models.IntegerField(default=1500)

    def __str__(self):
        return self.user.username
