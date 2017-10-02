# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
from problems.models import Problems,TestCases
#import django.db.models.signals.post_init


grader_running = 0
# Create your models here.
class Queue(models.Model):
    name = models.CharField(max_length=20)
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
    lang_choices = (
        ('C++' , 'C++'),
        ('Java', 'Java'),
        ('C' , 'C'),
        ('Py2' , 'Python 2'),
        ('Py3' , 'Python 3')
    )
    lang = models.CharField(max_length=4,choices=lang_choices)
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

    def __init__(self, *args, **kwargs):
        print('in')
        if (not grader_running): grader()
        super(Submission, self).__init__(*args, **kwargs)

def grader():
    grader_running = 1
    queue = Queue.objects.get(pk=1)
    while(queue.submission_set.filter(status='P').count()):# || Queue.submission_set.filter(phase='R')):
        queue.submission_set.all()[0].status = 'C'
        queue.submission_set.all()[0].verdict = 'Accepted'
        #if (submission==NULL) : print('a')
        #else : print('b')
        #bashfunc(pending_submission)
        #submission.status = 'C'
        #submission.verdict = 'Accepted'
    grader_running = 0
