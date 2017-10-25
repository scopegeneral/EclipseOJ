# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Queue,Submission
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
def main(request):
    # main_queue = Queue.objects.all()[0].submission_set.order_by('submission_time')
    submission_list = Submission.objects.order_by('-submission_time')
    return render(request,'judge/index.html',{'submission_list' : submission_list})

def userspecific(request,username):
    if User.objects.filter(username = username).exists():
        submission_list = Submission.objects.filter(user__username = username).order_by('-submission_time')
        return render(request, 'judge/index.html', {'submission_list' : submission_list, 'username' : username})
    else:
        return render(request, 'warning.html', {'warning': "No such user exists", 'message': "Please verify your details and try again."})
