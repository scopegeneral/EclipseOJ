from django.db import models
from contests.models import Contest
import datetime
from django.core.validators import RegexValidator

class Problem(models.Model):
    class Meta:
        verbose_name_plural = "Problems"
    contest = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
        limit_choices_to={'end_time__gt': datetime.datetime.now()},
    )
    #models.CASCADE deletes the Problems of contest if that particular contest is deleted
    # contest_alpha = models.CharField(max_length=1)
    problem_ID = models.CharField(max_length=10, unique=True)       ###redutry do without it #later
    number = models.CharField(max_length=1, validators=[RegexValidator(r'^[A-Z]$', 'Only Captial letter is allowed.')])
    name = models.CharField(max_length=40)
    body = models.TextField()

    def save(self):
        self.problem_ID = str(self.contest.id)+str(self.number)
        super().save()

    def __str__(self):
        return self.name #+ '\n' + self.problem_body

def testcases_directory_path(instance, filename):
    return 'testcases/testcases_{0}/{1}'.format(instance.problem.problem_ID, filename)

class TestCase(models.Model):
    class Meta:
        verbose_name_plural = "TestCases"
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    testcase_body = models.FileField(upload_to=testcases_directory_path)
