from django.db import models
from contest.models import Contest
# Create your models here.
class Problems(models.Model):
    contest = models.ForeignKey(Contest,on_delete=models.CASCADE)
    #models.CASCADE deletes the Problems of contest if that particular contest is deleted
    contest_alpha = models.CharField(max_length=1)
    problemID = models.CharField(max_length=10)       ###redutry do without it #later
    problem_name = models.CharField(max_length=40)
    problem_body = models.TextField()
    def __str__(self):
        return self.problem_name #+ '\n' + self.problem_body


class TestCases(models.Model):
    problem = models.ForeignKey(Problems,on_delete=models.CASCADE)
    testcase_body = models.TextField()
    def __str__(self):
        return self.testcase_body
