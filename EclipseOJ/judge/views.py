# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Queue,Submission
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
def main(request):
    """
    This is the submissions view. You can see the latest submissions inserted into submission queue of system. This displays list of submission of all users sorted via time. The submissions of logged in user are highlighted

    **Template:**

    :template:`judge/index.html`
    """
    submission_list = Submission.objects.order_by('-submission_time')
    return render(request,'judge/index.html',{'submission_list' : submission_list})

def userspecific(request,username):
    """
    This is the submissions view for a particular user. You can see the latest submissions by user inserted into submission queue of system. This displays list of submission of particular users sorted via time. The submissions are highlighted based on verdicts provided to submissions

    **Template:**

    :template:`judge/index.html`
    """
    if User.objects.filter(username = username).exists():
        submission_list = Submission.objects.filter(user__username = username).order_by('-submission_time')
        return render(request, 'judge/index.html', {'submission_list' : submission_list, 'username' : username})
    else:
        return render(request, 'warning.html', {'warning': "No such user exists", 'message': "Please verify your details and try again."})
