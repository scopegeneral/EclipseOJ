from django.shortcuts import render
from .models import Contest
from django.http import Http404
from problems.models import Problem
from datetime import datetime
from django.template.context_processors import csrf

now = datetime.now()
def index(request):
    past_contests = Contest.objects.filter(end_time__lt=datetime.now())
    current_contests = Contest.objects.filter(start_time__lt=datetime.now(), end_time__gt=datetime.now())
    upcoming_contests = Contest.objects.filter(start_time__gt=datetime.now())
    return render(request,"contests/index.html", {'past_contests':past_contests, 'current_contests':current_contests, 'upcoming_contests':upcoming_contests, })

def contest(request,contestID):
    try:
        contest = Contest.objects.get(pk=contestID)
    except Contest.DoesNotExist:
        raise Http404("There is no such contest :/ Please check again :P")
    if contest.start_time.strftime('%Y-%m-%d %H:%M') <= now.strftime('%Y-%m-%d %H:%M'):
        problems = Problem.objects.filter(contest=contest).order_by('letter')
        return render(request,"contests/contest.html", {'contest':contest, 'problems':problems})
    else:
        if request.method=='POST':
            contest.registered_user.add(request.user)
            print(request.user.username)
        args = {}
        args.update(csrf(request))
        args['contest'] = contest
        return render(request,"contests/notactive.html", args)
