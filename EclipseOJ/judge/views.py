# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Queue,Submission
from django.shortcuts import render

# Create your views here.
def main(request):
    main_queue = Queue.objects.get(pk=1)
    return render(request,'judge/main.html',{'main_queue' : main_queue})

def userspecific(request,username):
    main_queue = Queue.objects.get(pk=1)
    return render(request,'judge/userspecific.html',{'main_queue' : main_queue, 'username' : username})
