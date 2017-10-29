from django.shortcuts import render
from core.models import Profile
from django.http import HttpResponseRedirect
from .forms import SearchForm
from contests.models import Contest, Score
from leaderboard.models import rating_update
from django.template.context_processors import csrf

def index(request):
    """
    Displays the leaderboard, the ranking of users based on their ratings. Users are sorted based on here ratings in decreasing order, i.e. highest rating first. You can also search for any class of users according to their insitution country cirty etc.

    **Template:**

    :template:`leaderboard/index.html`
    """
    all_users = Profile.objects.all().order_by('-rating')
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            userID = form.cleaned_data['userID']
            countryID = form.cleaned_data['countryID']
            cityID = form.cleaned_data['cityID']
            instiID = form.cleaned_data['instiID']
            params = ('userID', 'countryID', 'cityID', 'instiID')
            args = {}
            if userID:
                all_users = all_users.filter(user__username = userID)
            if countryID:
                all_users = all_users.filter(country = countryID)
            if cityID:
                all_users = all_users.filter(city = cityID)
            if instiID:
                all_users = all_users.filter(institute = instiID)
            for param in params:
                args[param] = eval(param)
            if all_users:
                form = SearchForm()
                args['all_users'] = all_users
                args['form'] = form
                args.update(csrf(request))
                return render(request, 'leaderboard/index.html', args)
            else:
                args = {}
                args['warning'] = "No match for the query found"
                args['message'] = "Please verify your details and try again."
                return render(request, 'warning.html', args)
    else:
        form = SearchForm()
        if all_users:
            args = {}
            args.update(csrf(request))
            args['all_users'] = all_users
            args['form'] = form
            return render(request, 'leaderboard/index.html', args)
        else:
            args = {}
            args['warning'] = 'No Users were found in the database.'
            args['next'] = request.GET.get("next", False)
            return render(request, 'warning.html', args)

def contest_ranks(request,contestID):
    """
    This is the ranking based on the performance of users in particular contest. The contests scores are calculated and ranking is created.

    **Template:**

    :template:`leaderboard/contest_scores.html`
    """
    contest=Contest.objects.get(id=contestID)
    contest_scores=Score.objects.filter(contest=contest).order_by('-score')
    return render(request, 'leaderboard/contest_scores.html',{'contest_ID':contestID,'contest_scores' : contest_scores})
