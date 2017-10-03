from django.shortcuts import render
from .models import Problem, TestCase
from django.http import Http404

# Create your views here.
def index(request):
    all_problems = Problem.objects.all()
    return render(request,"problems/index.html", {'all_problems' : all_problems})

def problem(request, problemID):
    try:
        problem = Problem.objects.get(problem_ID=problemID)
    except Problem.DoesNotExist:
        raise Http404("There is no such problem :/ Please check again :P")
    return render(request,"problems/problem.html", {'problem' : problem})
