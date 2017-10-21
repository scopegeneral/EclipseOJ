from django.shortcuts import render
from accounts.models import Profile
from django.http import HttpResponseRedirect
from .forms import SearchForm
from contests.models import Contest, Score
from leaderboard.models import rating_update
def index(request):
    all_users = Profile.objects.all()
    rating_update(1)
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            userID = form.cleaned_data['userID']
            countryID = form.cleaned_data['countryID']
            cityID = form.cleaned_data['cityID']
            instiID = form.cleaned_data['instiID']
            return HttpResponseRedirect("search/{0}/{1}/{2}/{3}/".format(userID, countryID, cityID, instiID))

    else:
        form = SearchForm()
        return render(request, 'leaderboard/index.html', {'all_users' : all_users,'form': form})


def search(request,userID,countryID,cityID,instiID):
    all_users = Profile.objects.all()
    if userID:
        all_users = all_users.filter(user__username = userID)
    if countryID:
        all_users = all_users.filter(country = countryID)
    if cityID:
        all_users = all_users.filter(city = cityID)
    if instiID:
        all_users = all_users.filter(institute = instiID)
    return render(request, 'leaderboard/search.html', {'all_users' : all_users})

def contest_ranks(request,contestID):
    contest=Contest.objects.get(id=contestID)
    contest_scores=Score.objects.filter(contest=contest)
    return render(request, 'leaderboard/contest_scores.html',{'contest_scores' : contest_scores})
