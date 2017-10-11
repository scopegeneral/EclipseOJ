# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Queue,Submission
from django.shortcuts import render

# Create your views here.
def main(request):
    # main_queue = Queue.objects.all()[0].submission_set.order_by('submission_time')
    submission_list = Submission.objects.order_by('-submission_time')
    return render(request,'judge/main.html',{'submission_list' : submission_list})

def userspecific(request,username):
    submission_list = Submission.objects.order_by('-submission_time')
    return render(request,'judge/userspecific.html',{'submission_list' : submission_list, 'username' : username})
