from django.db import models
from django.contrib.auth.models import User
from accounts.models import Profile
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
    def __str__(self):
        return 'Contest '+str(contest.id)+': User'+str(user.username)
