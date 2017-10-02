from django.shortcuts import render
from .models import Contest
from django.http import Http404
from datetime import datetime
from problems.models import Problem

def index(request):
    past_contests = Contest.objects.filter(end_time__lt=datetime.now())
    current_contests = Contest.objects.filter(start_time__lt=datetime.now(), end_time__gt=datetime.now())
    upcoming_contests = Contest.objects.filter(start_time__gt=datetime.now())
    return render(request,"contests/index.html", {'past_contests':past_contests, 'current_contests':current_contests, 'upcoming_contests':upcoming_contests, })

def contest(request,contestID):
    try:
        contest = Contest.objects.get(contest_ID=contestID)
    except Contest.DoesNotExist:
        raise Http404("There is no such contest :/ Please check again :P")
    problems = Problem.objects.filter(contest=contest).order_by('number')
    return render(request,"contests/contest.html", {'contest':contest, 'problems':problems})
