from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
from array import *
import django.dispatch
from datetime import datetime
from django.dispatch import receiver
now=datetime.now()

contest_done = django.dispatch.Signal(providing_args=['contestID'])
class Contest(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    registered_user = models.ManyToManyField(User, blank = True, null = True)
    name = models.CharField(max_length=200,blank=True)
    def send_contest(self):
        if contest.end_time.strftime('%Y-%m-%d %H:%M') == now.strftime('%Y-%m-%d %H:%M'):
            contest_done.send(sender=self.__class__,contestID=self.id)
    def __str__(self):
        return 'Contest '+str(self.id)


@receiver(contest_done, sender=Contest)
def rating_updater(sender, **kwargs):
    print(kwargs.get('contestID'))
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
