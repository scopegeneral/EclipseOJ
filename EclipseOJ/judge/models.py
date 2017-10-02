# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
#from problems.model import Problems,Testcases

"""Commented some code here as problems arent from this branch"""

# Create your models here.
class Queue(models.Model):
    queue_name = models.CharField(max_length=20)
    """
        this is the central queue
        only 1 queue will be created and submissions will be foreign_key linked to it
    """



class Submission(models.Model):
    queue = models.ForeignKey(Queue,on_delete=models.CASCADE)
    problemid = models.CharField(max_length=10)
    userid = models.CharField(max_length=160)
    submission_time = models.DateTimeField(default=now())
    status_choices = (
        ('P' , 'Pending'),
        ('R' , 'Running'),
        ('C' , 'Completed')
    )
    status = models.CharField(max_length=1,choices=status_choices,default='P')
    #total_test_cases = models.IntegerField(default=Problems.object.get(problemID=problemid).testcases_set.size)
    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^check once abhi cant compile :P
    testcases_passed = models.IntegerField(default=0)
    verdict = models.CharField(max_length=20,default='Pending')
    def __str__(self):
        if self.status == 'Pending':
            return self.problemid + ': ' + 'Pending'
        elif self.status == 'Running':
            return self.problemid + ': ' + 'Running on ' + str(testcases_passed + 1)
        else :
            return self.problemid + ': ' + self.verdict
