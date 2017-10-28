from django.db import models
from contests.models import Contest
import datetime
from django.core.validators import RegexValidator

class Problem(models.Model):
    """
    This model is built for storing the problem to solve. It stores basic features and properties for a problem.
    """
    contest = models.ForeignKey(
        Contest,
        on_delete=models.CASCADE,
        limit_choices_to={'end_time__gt': datetime.datetime.now()},
        help_text="A Problem is linked to Contest model i.e. it belongs to a contest. ForeignKey mechanism has been provided to create a link between contest object and problem object. The on_delete = CASCADE has been set to true, which means if a contest is deleted it's constituting problems will be also deleted automatically. Also a contest can be only linked through ForeignKey if end time of contest is greater than the current time. ",
    )
    problem_ID = models.CharField(
        max_length=10,
        unique=True,
        #help_text="This "
    )
    letter = models.CharField(
        max_length=1,
        validators=[RegexValidator(r'^[A-Z]$', 'Only a captial letter is allowed.')],
        help_text="Each contest may contain number of problems (in general 5 or 6). Problems in a particular contest are distnguished/uniquified by a problem id which is a single captial letter",
    )
    name = models.CharField(
        max_length=40,
        help_text="It is used for storing the name of problem, in a Char field. The maximum length for problem name has been set to 40",
    )
    body = models.TextField(
        help_text="This is the core of problem, ie used for storing the problem statement and relevant stuff like input output characterstics and and sample test cases. This takes input as a html text and is rendered through the safe tag in django template language. This may contain mathematical equations which are rendered through MathJX",
    )
    timelimit = models.FloatField(
        default=1,
        help_text="This is the timelimit for which a particular testcase can run. This prevents slow and inefficient codes from being marked correct."
    )
    marks=models.IntegerField(
        default=0,
        help_text="This stored marks that will be awarded to user on solving the problem during contest",
    )
    solved=models.IntegerField(
        default=0,
        help_text="This stores how many users have succesfully solved the problem. Get's updated through server mechanism.",
    )
    def save(self):
        self.problem_ID = str(self.contest.id)+str(self.letter)
        super().save()

    def __str__(self):
        return self.name

def testcases_input_path(instance, filename):
    return 'testcases/{0}/input_{1}'.format(instance.problem.problem_ID, instance.testcase_ID)

def testcases_output_path(instance, filename):
    return 'testcases/{0}/output_{1}'.format(instance.problem.problem_ID, instance.testcase_ID)

class TestCase(models.Model):
    """
    This model is built for storing test cases. A testcase in progrmming contests is used to check wether the user has submitted a correct solution or not and wether he has covered all the boundary cases or not. It contains input and output. A user submitted solution when runs through a test case, input is provided to the program through STDIN and output is tunneled throught STDOUT to a temporary text file which is latter compared with current output
    """
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        help_text="A TestCase is linked to Problem model i.e. it belongs to a problem. ForeignKey mechanism has been provided to create a link between contest object and problem object. The on_delete = CASCADE has been set to true, which means if a problem is deleted it's constituting testcases will be also deleted automatically.",
    )
    testcase_ID = models.PositiveIntegerField(
        help_text="Problem may contain many test cases so to uniquigy a testcase a testcase property has been provided. For checking the submission we loop through test cases based on testcase id's",
    )
    input_file = models.FileField(
        upload_to=testcases_input_path,
        help_text="This is a FileField and stores the input file to be used for checking procedure. The file is uploaded to a testcases subdirectory in the uploads directory with the name input_(testcase id)."
    )
    output_file = models.FileField(
        upload_to=testcases_output_path,
        help_text="This is a FileField and stores the output file to be used for checking procedure. The file is uploaded to a testcases subdirectory in the uploads directory with the name output_(testcase id)."
    )

    class Meta:
        unique_together = ("problem", "testcase_ID")
    def __str__(self):
        return 'Problem: {0} Testcase: {1}'.format(self.problem.problem_ID, self.testcase_ID)
