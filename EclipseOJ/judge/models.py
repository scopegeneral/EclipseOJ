# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from problems.models import Problem, TestCase
from django.contrib.auth.models import User
from django.db.models import signals
from django.dispatch import Signal
import os, re
from contests.models import Score, Contest
import docker
from subprocess import Popen, PIPE
client = docker.from_env()
container = client.containers.get('dock_container')
os.system("docker cp check.py " + container.short_id + ":/")
os.system("docker cp sandbox.sh " + container.short_id + ":/")

# Create your models here.
class Queue(models.Model):
    """
    Queues are a basic objects used to provide a queue kind of hierarchy in checking procedure. They are used for storing :model:`judge.Submission` asynchronously grading of submission. The queues have been built analogous to how Celery uses RabbitMQ. So basically the grader function runs on a queue, one by one probes the ungraded submissions in particular queue (by the submission time), grades it and provides the verdict  to the submission. There are three queues present in the system and submissions are accordingly distributed to one of the queue. Each time a :model:`judge.Submission` is created, if all Submissions in queue are checked, a new thread is created and grader function which provides verdict to submissions is called in the new thread for providing asynchronous mechanism. Otherwise if grader is already running then the submission would automatically be graded at later time.
    """
    name = models.CharField(
        max_length=20,
        help_text="This is used to store the name of queue",
    )
    def __str__(self):
        return 'Queue {}: {}'.format(self.id, self.name)


def upload_to(instance, filename):
    directory = os.path.join(os.path.join(os.getcwd(), 'uploads/users/'), instance.user.username)
    for f in os.listdir(directory):
        if os.path.splitext(f)[0] == 'solution' + instance.problem.problem_ID:
            os.remove(os.path.join(directory, f))
    return 'users/%s/%s.%s' % (instance.user.username, 'solution' + instance.problem.problem_ID, instance.language)

class Submission(models.Model):
    """
    A submission object is a reference to the solution of user. It stores the properties related to solution and links the checking procedure to frontend. Basically whenever a solution is created (a solution is created when user submits code on website), the checking function "grader is called" which runs on a queue asynchronously
    """
    queue = models.ForeignKey(
        Queue,
        on_delete=models.CASCADE,
        help_text="A Submission is linked to Queue model i.e. it belongs to a particular queue. ForeignKey mechanism has been provided to create a link between contest object and problem object.",
    )
    problem = models.ForeignKey(
        Problem,
        on_delete=models.CASCADE,
        help_text="A Submission is linked to Problem model i.e. it belongs to a particular problem. ForeignKey mechanism has been provided to create a link between submission object and problem object. The on_delete = CASCADE has been set to true, which means if a problem is deleted it's related submissions will be also deleted automatically.",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        help_text="A Submission is linked to User model i.e. it belongs to a particular user. ForeignKey mechanism has been provided to create a link between submission object and user object. The on_delete = CASCADE has been set to true, which means if a user is deleted all his submissions will be also deleted automatically.",
    )
    uploaded_file = models.FileField(
        upload_to=upload_to,
        help_text="Submission is stored in form of FileField. the file is either obtained using direct file submission from the user or by extracting text from the editor provided on a website. The solutions is uploaded to user subdirectory in the uploads directory",
    )
    submission_time = models.DateTimeField(
        auto_now_add=True,
        help_text="This is a DateTimeField and is used to store the time of submission of user",
    )
    lang_choices = (
        ('cpp' , 'C++'),
        ('java', 'Java'),
        ('c' , 'C'),
        ('py' , 'Python 2'),
        ('py3' , 'Python 3')
    )
    language = models.CharField(
        max_length=4,
        choices=lang_choices,default='cpp',
        help_text="It is used to store which language has the solution been submitted. 5 choices for the language have been provided as c++, Java, Python2, Python3, C",
    )
    testcases_passed = models.IntegerField(
        default=0,
        help_text="It is used to store the number of testcases passed by the user. It defaults to 0",
    )
    verdict_choices = (
        ('Q', 'In queue'),
        ('R', 'Running'),
        ('WA', 'Wrong Answer'),
        ('CE', 'Compilation Error'),
        ('RE', 'Runtime Error'),
        ('AC', 'Accepted'),
        ('TLE', 'Time Limit Exceeded'),
    )
    verdict = models.CharField(
        max_length=3,
        choices=verdict_choices,
        default='Q',
        help_text="The verdict of the submission tells wether the solution is correct or incorrect or is still not been checked. 7 choices have been provided for the verdict. 'In queue' tells that the solution has not yet been checked. 'Running tells that the solutions is under process of being graded. 'Wrong Answer' tells that the solution gave wrong answer at some testcase. 'Compilation Error' tells that the solution didnt even compile. 'Runtime Error' tells that there was a runtime error in between grading. 'Time Limit Exceeded' verdict means that solutions exceeded the timelimit set for the problem under some test case. 'Accepted' means that the solution is correct",
    )
    def __str__(self):
        return self.problem.problem_ID + ': ' + self.verdict

grader_running = [False,False,False]
last_queue = 2
def grader(queue_number):
    grader_running = True
    queue = Queue.objects.all()[queue_number]
    while(queue.submission_set.filter(verdict='Q').exists()):
        submission = queue.submission_set.filter(verdict='Q').order_by('submission_time')[0]
        submission.verdict = 'R'
        print(str(submission))
        testcase = "uploads/testcases/{0}/".format(submission.problem.problem_ID)+" "
        filename='uploads/'+submission.uploaded_file.name+' '
        number=TestCase.objects.filter(problem=submission.problem).count()
        os.system("docker exec -it dock_container mkdir -p "+ os.path.dirname(filename))
        os.system("docker cp "+ filename + container.short_id + ":/"+os.path.dirname(filename))
        os.system("docker cp " + testcase + container.short_id + ":/uploads/testcases/")
        os.system("echo "+filename+ " > inputs")
        os.system("echo "+testcase+" >> inputs ")
        os.system("echo "+str(number)+" >> inputs")
        os.system("echo "+submission.language+" >> inputs")
        os.system("echo "+str(submission.problem.timelimit)+" >> inputs")
        os.system("docker cp inputs " + container.short_id + ":/")
        process=Popen("docker exec -i dock_container sh -c './sandbox.sh'",shell=True,stdout=PIPE)
        os.system('rm inputs')
        submission.verdict=process.stdout.read().strip().decode("utf-8")
        if submission.verdict == 'AC':
            try:
                score=Score.objects.get(contest=submission.problem.contest,user=submission.user)
                if ord(submission.problem.letter)-65 == 0 and score.acceptedA == 0:
                    score.score += submission.problem.marks
                    score.acceptedA=True
                    submission.problem.solved += 1
                    submission.problem.save()
                    score.save()
                elif ord(submission.problem.letter)-65 == 1 and score.acceptedB == 0:
                    score.score += submission.problem.marks
                    score.acceptedB=True
                    submission.problem.solved += 1
                    submission.problem.save()
                    score.save()
                elif ord(submission.problem.letter)-65 == 2 and score.acceptedC == 0:
                    score.score += submission.problem.marks
                    score.acceptedC=True
                    submission.problem.solved += 1
                    submission.problem.save()
                    score.save()
                elif ord(submission.problem.letter)-65 == 3 and score.acceptedD == 0:
                    score.score += submission.problem.marks
                    score.acceptedD=True
                    submission.problem.solved += 1
                    submission.problem.save()
                    score.save()
                elif ord(submission.problem.letter)-65 == 4 and score.acceptedE == 0:
                    score.score += submission.problem.marks
                    score.acceptedE=True
                    submission.problem.solved += 1
                    submission.problem.save()
                    score.save()
                elif ord(submission.problem.letter)-65 == 5 and score.acceptedF == 0:
                    score.score += submission.problem.marks
                    score.acceptedF=True
                    submission.problem.solved += 1
                    submission.problem.save()
                    score.save()
            except Score.DoesNotExist:
                print('something')
        submission.save()
    grader_running = False
