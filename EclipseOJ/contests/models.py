from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from array import *
class Contest(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    registered_user = models.ManyToManyField(User, blank = True, null = True)
    name = models.CharField(max_length=200,blank=True)
    def __str__(self):
        return 'Contest '+str(self.id)


class Score(models.Model):
    contest=models.ForeignKey(Contest)
    user=models.ForeignKey(User)
    score=models.IntegerField(default=0)
    acceptedA=models.IntegerField(default=0)
    acceptedB=models.IntegerField(default=0)
    acceptedC=models.IntegerField(default=0)
    acceptedD=models.IntegerField(default=0)
    acceptedE=models.IntegerField(default=0)
    acceptedF=models.IntegerField(default=0)
    wins=models.IntegerField(default=0)
    def __str__(self):
        return 'Contest '+str(self.contest.id)+': User'+str(self.user.username)
