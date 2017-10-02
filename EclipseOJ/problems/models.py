from django.db import models
from contest.models import Contest
# Create your models here.
class Problems(models.Model):
    class Meta:
        verbose_name_plural = "Problems"
    contest = models.ForeignKey(Contest,on_delete=models.CASCADE)
    #models.CASCADE deletes the Problems of contest if that particular contest is deleted
    contest_alpha = models.CharField(max_length=1)
    problemID = models.CharField(max_length=10)       ###redutry do without it #later
    problem_name = models.CharField(max_length=40)
    problem_body = models.TextField()
    def __str__(self):
        return self.problem_name #+ '\n' + self.problem_body

def testcases_directory_path(instance, filename):
    return 'testcases/testcases_{0}/{1}'.format(instance.problem.problemID, filename)

class TestCases(models.Model):
    class Meta:
        verbose_name_plural = "TestCases"
    problem = models.ForeignKey(Problems,on_delete=models.CASCADE)
    testcase_body = models.FileField(upload_to=testcases_directory_path)
