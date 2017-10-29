from django.db import models
from django.contrib.auth.models import User
from core.models import Profile
from array import *
from datetime import datetime
from django.utils import timezone

class Contest(models.Model):
    """
    Contests models are used to store save contests as object. Contests contain problems, users register in a contest and that's how they can compete among one another.
    """
    start_time = models.DateTimeField(
        help_text="This is a DateTimeField used to store start time of contest"
    )
    end_time = models.DateTimeField(
        help_text="This is a DateTimeField used to store end time of contest"
    )
    registered_user = models.ManyToManyField(
        User, blank = True,
        help_text="This is a ManyToManyField field between :model:`auth.User` and contest. Multiple users will register any contests, this field anables direct access to list of users registered for contests. Also this stores in users which contests they registered for"
    )
    name = models.CharField(
        max_length=200,
        blank=True,
        help_text="This is the name of the contest"
    )
    completed = models.BooleanField(
        default=False,
        help_text="This is a boolean variable that automatically gets updated once the contests is completed."
    )
    def __str__(self):
        return 'Contest {}: {}'.format(str(self.id), self.name)


class Score(models.Model):
    """
    Score models are used to store the performance of a particular user in a particular contest.
    """
    contest=models.ForeignKey(
        Contest,
        help_text="This is a ForeignKey relation betwen a Score object and a Contest object. The tells us that a Score model is linked to a particular contest"
    )
    user=models.ForeignKey(
        User,
        help_text="This is a ForeignKey relation betwen a Score object and a Contest object. The tells us that a Score model belongs to which user",
    )
    score=models.IntegerField(
        default=0,
        help_text="This is the score of user in a particular contest. This is calculated by checking number of problems he solved and  duration it took him to solve the problems"
    )
    acceptedA=models.BooleanField(
        default=False,
        help_text="Boolean field whether A is solved or not",
    )
    acceptedB=models.BooleanField(
        default=False,
        help_text="Boolean field whether B is solved or not",
    )
    acceptedC=models.BooleanField(
        default=False,
        help_text="Boolean field whether C is solved or not",
    )
    acceptedD=models.BooleanField(
        default=False,
        help_text="Boolean field whether D is solved or not",
    )
    acceptedE=models.BooleanField(
        default=False,
        help_text="Boolean field whether E is solved or not",
    )
    acceptedF=models.BooleanField(
        default=False,
        help_text="Boolean field whether F is solved or not",
    )
    wins=models.IntegerField(
        default=0,
        help_text="It keeps track of the number of users he defeated"
    )
    def __str__(self):
        return 'Contest '+str(self.contest.id)+': User '+str(self.user.username)
