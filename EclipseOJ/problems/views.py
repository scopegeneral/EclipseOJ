from .models import Problem, TestCase
from . import forms as problems_forms
from django.http import Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.context_processors import csrf
from django.contrib.auth.models import User
from judge.models import *
from judge.models import last_queue
from django.core.files.base import ContentFile
import threading
from datetime import datetime
from django.utils.six.moves.urllib.parse import urlencode
# Create your views here.
now = datetime.now()
def index(request):
    all_problems = Problem.objects.all()
    return render(request,"problems/index.html", {'all_problems' : all_problems})

def problem(request, problemID):
    try:
        problem = Problem.objects.get(problem_ID=problemID)
    except Problem.DoesNotExist:
        raise Http404("There is no such problem. Please check again")

    if request.method == 'POST':
        submit_form = problems_forms.SubmitForm(request.POST, request.FILES)
        code_form = problems_forms.CodeForm(request.POST)
        if submit_form.is_valid():
            global last_queue
            last_queue = (last_queue + 1)%3
            submission = Submission()
            submission = submit_form.save(commit=False)
            submission.user = User.objects.get(username=request.user)
            submission.problem = problem
            submission.queue = Queue.objects.all()[last_queue]
            submission.save()
            messages.success(request, 'Successfully Submitted')
            """if not grader_running :
                #print('gonna call')
                t = threading.Thread(target=grader)
                t.start()
                #print('probably')
            """
            if not grader_running[last_queue]:
                t = threading.Thread(target=grader,kwargs={'queue_number':last_queue})
                t.start()
            return redirect(reverse('mysubmissions', kwargs={'username':request.user}))
        elif code_form.is_valid():
            #print(2)
            global last_queue
            last_queue = (last_queue + 1)%3
            data = code_form.cleaned_data
            submission = Submission()
            submission.language = data['lang']
            submission.user = User.objects.get(username=request.user)
            submission.problem = problem
            submission.queue = Queue.objects.all()[last_queue]
            submission.uploaded_file.save('arbit',ContentFile(data['code']))
            submission.save()
            print(data['lang'])
            messages.success(request, 'Successfully Submitted')
            if not grader_running[last_queue]:
                t = threading.Thread(target=grader,kwargs={'queue_number':last_queue})
                t.start()
            return redirect(reverse('mysubmissions', kwargs={'username':request.user}))
        else:
            print([(field.label, field.errors) for field in submit_form] )
            messages.warning(request, 'There was an error. Please check!')
    args = {}
    args.update(csrf(request))
    args['submit_form'] = problems_forms.SubmitForm()
    args['code_form'] = problems_forms.CodeForm()
    args['problem'] = problem
    contest = problem.contest
    args['contest'] = contest
    if contest.start_time.strftime('%Y-%m-%d %H:%M') <= now.strftime('%Y-%m-%d %H:%M'):
        return render(request,"problems/problem.html", args)
    elif contest.end_time.strftime('%Y-%m-%d %H:%M') <= now.strftime('%Y-%m-%d %H:%M'):
        registered = contest.registered_user.filter(username = request.user.username)
        args['registered'] = registered
        return render(request,"problems/isactive.html", args)
    else:
        raise Http404("There is no such problem you prick, you can't hack the system the system hacks you -_- !!")
