from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
class Contest(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    registered_user = models.ManyToManyField(User, blank = True, null = True)
    def __str__(self):
        return 'Contest '+str(self.id)
