from django.db import models
from contests.models import Score, Contest
from core.models import Profile
# Create your models here.

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
    for score in contest_scores:
        profile=score.user.profile
        profile.rating = (total_score-profile.rating + 400*score.wins)/games
        profile.save()
