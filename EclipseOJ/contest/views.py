from django.shortcuts import render
# Create your views here.
from .models import Contest
from django.http import Http404


def index(request):
    all_contest = Contest.objects.all()
    return render(request,"contest/index.html", {'all_contest' : all_contest})

def contest(request,contestID):
    try:
        contest = Contest.objects.get(contest_id=contestID)
    except Contest.DoesNotExist:
        raise Http404("There is no such contest :/ Please check again :P")
    return render(request,"contest/contest.html", {'contest' : contest})
