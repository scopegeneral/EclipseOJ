from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from array import *
from datetime import datetime
from django.utils import timezone
class Contest(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    registered_user = models.ManyToManyField(User, blank = True, null = True)
    name = models.CharField(max_length=200,blank=True)
    completed = models.BooleanField(default=False)
    def __str__(self):
        return 'Contest '+str(self.id)


class Score(models.Model):
    contest=models.ForeignKey(Contest)
    user=models.ForeignKey(User)
    score=models.IntegerField(default=0)
    acceptedA=models.BooleanField(default=False)
    acceptedB=models.BooleanField(default=False)
    acceptedC=models.BooleanField(default=False)
    acceptedD=models.BooleanField(default=False)
    acceptedE=models.BooleanField(default=False)
    acceptedF=models.BooleanField(default=False)
    wins=models.IntegerField(default=0)
    def __str__(self):
        return 'Contest '+str(self.contest.id)+': User '+str(self.user.username)
