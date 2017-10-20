# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from problems.models import Problem, TestCase
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import Signal
import os, re
from .check import bashfunc

# Create your models here.
class Queue(models.Model):
    name = models.CharField(max_length=20)
    """
        this is the central queue
        only 1 queue will be created and submissions will be foreign_key linked to it
    """


def upload_to(instance, filename):
    directory = os.path.join(os.path.join(os.getcwd(), 'uploads/users/'), instance.user.username)
    for f in os.listdir(directory):
        if os.path.splitext(f)[0] == 'solution' + instance.problem.problem_ID:
            os.remove(os.path.join(directory, f))
    return 'users/%s/%s.%s' % (instance.user.username, 'solution' + instance.problem.problem_ID, instance.language)

class Submission(models.Model):
    queue = models.ForeignKey(Queue,on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    uploaded_file = models.FileField(upload_to=upload_to)
    submission_time = models.DateTimeField(auto_now_add=True)
    lang_choices = (
        ('cpp' , 'C++'),
        ('java', 'Java'),
        ('c' , 'C'),
        ('py' , 'Python 2'),
        ('py3' , 'Python 3')
    )
    language = models.CharField(max_length=4,choices=lang_choices,default='cpp')
    testcases_passed = models.IntegerField(default=0)
    verdict_choices = (
        ('Q', 'In queue'),
        ('R', 'Running'),
        ('WA', 'Wrong Answer'),
        ('CE', 'Compilation Error'),
        ('RE', 'Runtime Error'),
        ('AC', 'Accepted'),
    )
    verdict = models.CharField(max_length=2,choices=verdict_choices, default='Q')
    def __str__(self):
        if self.verdict == 'Q':
            return self.problem.problem_ID + ': ' + 'In queue'
        elif self.verdict == 'R':
            return self.problem.problem_ID + ': ' + 'Running'
        else :
            return self.problem.problem_ID + ': ' + self.verdict

def submission_post_save(sender, instance, created, *args, **kwargs):
    if not created:
        return
    if not grader_running:
        grader()
signals.post_save.connect(submission_post_save,sender=Submission)

grader_running = False
def grader():
    grader_running = True
    queue = Queue.objects.all()[0]
    #print('Hey buddy i have been called!')
    #print('before while')
    while(queue.submission_set.filter(verdict='Q').exists()):
        submission = queue.submission_set.filter(verdict='Q').order_by('submission_time')[0]
        submission.verdict = 'R'
        print(str(submission))
        testcase = "uploads/testcases/{0}/".format(submission.problem.problem_ID)
        submission.verdict = bashfunc('uploads/'+submission.uploaded_file.name, testcase, int(TestCase.objects.filter(problem=submission.problem).count()), submission.language, 2)
        #print('done')
        submission.save()
    grader_running = False
