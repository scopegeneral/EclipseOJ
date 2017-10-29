# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Queue,Submission
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
def main(request):
    """
    This is the submissions view. You can see the latest submissions inserted into submission queue of system. This displays list of submission of all users sorted via time. The submissions of logged in user are highlighted

    **Args:**

    1. submission_list
        It is a query set of all the submissions present in the system.

    **Template:**

    :template:`judge/index.html`
    """
    submission_list = Submission.objects.order_by('-submission_time')
    return render(request,'judge/index.html',{'submission_list' : submission_list})

def userspecific(request,username):
    """
    This is the submissions view for a particular user. You can see the latest submissions by user inserted into submission queue of system. This displays list of submission of particular users sorted via time. The submissions are highlighted based on verdicts provided to submissions

    **Args:**

    1. submission_list
        It is a query set of all the submissions present in the system.
    2. username
        It is username of user for which personalized submission-list has to seen    

    **Template:**

    :template:`judge/index.html`
    """
    if User.objects.filter(username = username).exists():
        submission_list = Submission.objects.filter(user__username = username).order_by('-submission_time')
        return render(request, 'judge/index.html', {'submission_list' : submission_list, 'username' : username})
    else:
        return render(request, 'warning.html', {'warning': "No such user exists", 'message': "Please verify your details and try again."})
