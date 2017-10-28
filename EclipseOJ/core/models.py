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
    """
    This is used to extend default :model:`auth.User` to store extra information about the people using the site.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        help_text="This is a OneToOneField relationship i.e. User and Profile are uniquly related. Profile extends the default User model. on_delete = CASCADE is true which means if User is deleted then the Profile will be deleted automatically",
    )
    picture = models.ImageField(
        upload_to=picture_path,
        default=static('default_picture.jpg'),
        blank=True,
        help_text="It is an ImageField and is used to store profile picture of user.",
    )
    first_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="First name of the user",
    )
    last_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Last name of the user",
    )
    email = models.EmailField(
        max_length=70,
        blank=True,
        help_text="This is the email id of the user. The EmailID validator provided by django is used",
    )
    country = CountryField(
        default='IN',
        blank=True,
        help_text="This is used to store the country of user. A third party package django-countries has been used which access to all countries. Default has been set to India",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        help_text="This is they city of the user",
    )
    institute = models.CharField(
        max_length=100,
        blank=True,
        help_text="This is the institute of the user",
    )
    rating = models.IntegerField(
        default=1500,
        help_text="Users can compete with each other and rating is the parameter used for competing with each other. Rating are updated after each contest through probabilistic analysis of the contest result",
    )

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user(sender, instance, created, **kwargs):
    if not created:
        return
    os.mkdir(os.path.join(os.path.join(os.getcwd(), 'uploads/users/'), instance.get_username()))
