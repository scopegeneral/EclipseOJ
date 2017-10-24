from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.staticfiles.templatetags.staticfiles import static
import os

def picture_path(instance, filename):
    return 'users/{}/{}'.format(instance.user.username, 'picture')

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to=picture_path, default=static('default_picture.jpg'), blank=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(max_length=70, null=True)
    country = CountryField(default='IN')
    city = models.CharField(max_length=100, null=True)
    institute = models.CharField(max_length=100, null=True)
    rating = models.IntegerField(default=1500)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if not created:
        return
    os.mkdir(os.path.join(os.path.join(os.getcwd(), 'uploads/users/'), instance.get_username()))
