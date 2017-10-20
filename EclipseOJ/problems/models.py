from django.db import models
from contests.models import Contest
import datetime
from django.core.validators import RegexValidator

class Problem(models.Model):
    contest = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
        limit_choices_to={'end_time__gt': datetime.datetime.now()},
    )
    #models.CASCADE deletes the Problems of contest if that particular contest is deleted
    # contest_alpha = models.CharField(max_length=1)
    problem_ID = models.CharField(max_length=10, unique=True)       ###redutry do without it #later
    letter = models.CharField("Problem ID", max_length=1, validators=[RegexValidator(r'^[A-Z]$', 'Only a captial letter is allowed.')])
    name = models.CharField(max_length=40)
    body = models.TextField()
    timelimit = models.FloatField(default=1)
    def save(self):
        self.problem_ID = str(self.contest.id)+str(self.letter)
        super().save()

    def __str__(self):
        return self.name #+ '\n' + self.problem_body

def testcases_input_path(instance, filename):
    return 'testcases/{0}/input_{1}'.format(instance.problem.problem_ID, instance.testcase_ID)

def testcases_output_path(instance, filename):
    return 'testcases/{0}/output_{1}'.format(instance.problem.problem_ID, instance.testcase_ID)

class TestCase(models.Model):
    problem = models.ForeignKey(Problem,on_delete=models.CASCADE)
    testcase_ID = models.PositiveIntegerField()
    input_file = models.FileField(upload_to=testcases_input_path)
    output_file = models.FileField(upload_to=testcases_output_path)

    class Meta:
        unique_together = ("problem", "testcase_ID")
    def __str__(self):
        return 'Problem: {0} Testcase: {1}'.format(self.problem.problem_ID, self.testcase_ID)
