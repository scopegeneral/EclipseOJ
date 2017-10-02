# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.utils.timezone import now
from problems.models import Problems,TestCases
from django.db.models import signals
from django.dispatch import Signal

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
    lang = models.CharField(max_length=4,choices=lang_choices,default='C')
    testcases_passed = models.IntegerField(default=0)
    verdict = models.CharField(max_length=20,default='Pending')
    def __str__(self):
        if self.status == 'Pending':
            return self.problemid + ': ' + 'Pending'
        elif self.status == 'Running':
            return self.problemid + ': ' + 'Running on ' + str(testcases_passed + 1)
        else :
            return self.problemid + ': ' + self.verdict

def submission_post_save(sender, instance, created, *args, **kwargs):
    if created:
        if (not grader_running): grader()

signals.post_save.connect(submission_post_save,sender=Submission)

def grader():
    grader_running = 1
    queue = Queue.objects.get(pk=1)
    #print('before while')
    while(queue.submission_set.filter(status='P').count()):
        #print(str(queue.submission_set.filter(status='P').count()))
        submission = queue.submission_set.filter(status='P').order_by('submission_time')[0]
        #print(submission)
        #bashfunc(pending_submission)
        submission.status = 'C'
        submission.verdict = 'Accepted'
        submission.save()
    grader_running = 0
