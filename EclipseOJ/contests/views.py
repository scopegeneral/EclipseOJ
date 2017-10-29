from django.shortcuts import render
from .models import Contest, Score
from django.http import Http404
from problems.models import Problem
from datetime import datetime
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from django.utils import timezone
from core.models import Profile
#now = timezone.make_aware(datetime.now(),timezone.get_default_timezone()).astimezone(timezone.utc)
def index(request):
    """
    Display list of all :model:`contests.Contest` objects. The contests are divided into two parts :

    1. Future contests
    2. Past contests

    This view enables the user to access all contests from one page and keeps him informed about upcoming contests as well.

    **Args:**

    1. ``past_contests``
            A query-set of contests. Stores contests that have been finished
    2. ``current_contests``
            A query-set of contests. Stores contests that are currently running
    3. ``upcoming_contests``
            Aa query-set of contests. Stores contests that will occur in future
    4. ``top_rated``
            A query-set of profiles. Stores users sorted by user ratings

    **Template:**

    :template:`contests/index.html`
    """
    past_contests = Contest.objects.filter(end_time__lt=timezone.now())
    current_contests = Contest.objects.filter(start_time__lt=timezone.now(), end_time__gt=timezone.now())
    upcoming_contests = Contest.objects.filter(start_time__gt=timezone.now())
    top_rated = Profile.objects.order_by('-rating')[:5]
    return render(request,"contests/index.html", {'past_contests':past_contests, 'current_contests':current_contests, 'upcoming_contests':upcoming_contests, 'toprated':top_rated })

def contest(request,contestID):
    """
    It is the detailed view for a particular contests.  This views enables you to access all problems in a particular contests. It has been divided into three parts and three different templates have been created for each of them

    1. Future contests
    2. Past contests
    3. Current contests

    Future contests allow user to register for the contest, past contests show the user list of problems while the current contests show the user the the problems in the contests with a onsite countdown clock, which when time finishes refreshes the contest page into past contests.

    **Args:**

    1. ``contest``
            An instance of a contest. Stores the properties cotnained by contest like problems, scores etc
    2. ``registered``
            A query-set of users. Stores the lsit of users registered for the contest.


    **Template:**

    1. :template:`contests/notactive.html`
    2. :template:`contests/contest.html`
    """
    try:
        contest = Contest.objects.get(pk=contestID)
        user = request.user
    except Contest.DoesNotExist:
        raise Http404("There is no such contest :/ Please check again :P")
    registered = contest.registered_user.filter(username = request.user.username)
    top_scores=Score.objects.filter(contest=contest).order_by('-score')[:5]
    if contest.end_time.strftime('%Y-%m-%d %H:%M:%S') <= timezone.make_aware(datetime.now(),timezone.get_default_timezone()).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'):
        problems = Problem.objects.filter(contest=contest).order_by('letter')
        if contest.completed == False:
            contest.completed=True
            rating_update(contest.id)
            contest.save()
        return render(request,"contests/contest.html", {'contest':contest, 'problems':problems, 'registered':registered, 'topscores':top_scores})
    elif timezone.make_aware(datetime.now(),timezone.get_default_timezone()).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S') >= contest.start_time.strftime('%Y-%m-%d %H:%M:%S'):
        problems = Problem.objects.filter(contest=contest).order_by('letter')
        return render(request,"contests/contest.html", {'contest':contest, 'problems':problems, 'registered':registered, 'topscores':top_scores})
    else:
        if request.method=='POST':
            contest.registered_user.add(request.user)
            contest.score_query-set.create(user=user,score=0)
            print(request.user.username)
        args = {}
        args.update(csrf(request))
        args['contest'] = contest
        args['registered'] = registered
        return render(request,"contests/notactive.html", args)

def contest_registered(request,contestID):
    """
    This view provides the list of registered users in a particular contests

    **Args:**

    1. ``contest``
            An instance of a contest. Stores the properties cotnained by contest like problems, scores etc
    2. ``registerd_user_list``
            A query-set of users. Stores the list of users registered for the contest.

    **Template:**

    :template:`contests/user_list.html`
    """
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
