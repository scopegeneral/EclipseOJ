from django.shortcuts import render
from .models import Contest, Score
from django.http import Http404
from problems.models import Problem
from datetime import datetime
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.utils import timezone
#now = timezone.make_aware(datetime.now(),timezone.get_default_timezone()).astimezone(timezone.utc)
def index(request):
    past_contests = Contest.objects.filter(end_time__lt=timezone.now())
    current_contests = Contest.objects.filter(start_time__lt=timezone.now(), end_time__gt=timezone.now())
    upcoming_contests = Contest.objects.filter(start_time__gt=timezone.now())
    return render(request,"contests/index.html", {'past_contests':past_contests, 'current_contests':current_contests, 'upcoming_contests':upcoming_contests, })

def contest(request,contestID):
    try:
        contest = Contest.objects.get(pk=contestID)
        user = request.user
    except Contest.DoesNotExist:
        raise Http404("There is no such contest :/ Please check again :P")
    registered = contest.registered_user.filter(username = request.user.username)
    if contest.end_time.strftime('%Y-%m-%d %H:%M') <= timezone.make_aware(datetime.now(),timezone.get_default_timezone()).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M'):
        problems = Problem.objects.filter(contest=contest).order_by('letter')
        if contest.completed == False:
            contest.completed=True
            rating_update(contest.id)
            contest.save()
        return render(request,"contests/contest.html", {'contest':contest, 'problems':problems, 'registered':registered})
    elif timezone.make_aware(datetime.now(),timezone.get_default_timezone()).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M') >= contest.start_time.strftime('%Y-%m-%d %H:%M'):
        problems = Problem.objects.filter(contest=contest).order_by('letter')
        return render(request,"contests/contest.html", {'contest':contest, 'problems':problems, 'registered':registered})
    else:
        if request.method=='POST':
            contest.registered_user.add(request.user)
            contest.score_set.create(user=user,score=0)
            print(request.user.username)
        args = {}
        args.update(csrf(request))
        args['contest'] = contest
        args['registered'] = registered
        return render(request,"contests/notactive.html", args)

def contest_registered(request,contestID):
    try:
        contest = Contest.objects.get(pk=contestID)
    except Contest.DoesNotExist:
        raise Http404("There is no such contest :/ Please check again :P")
    #registered = contest.registered_user.filter(username = request.user.username) ##boolean variable
    registerd_user_list = contest.registered_user.all();
    return render(request,"contests/user_list.html",{'contest':contest, 'registerd_user_list':registerd_user_list})

def rating_update(contestID):
    contest=Contest.objects.get(id=contestID)
    contest_scores=Score.objects.filter(contest=contest)
    total_score=0
    for score in contest_scores:
        total_score+=score.user.profile.rating
    for score1 in contest_scores:
        for score2 in contest_scores:
            if score1.score>score2.score:
                score1.wins += 1
            elif score1.score<score2.score:
                score1.wins -= 1
        score1.save()
    games=contest_scores.count()-1
    if games>0:
        for score in contest_scores:
            profile=score.user.profile
            profile.rating = (total_score-profile.rating + 400*score.wins)/games
            profile.save()
