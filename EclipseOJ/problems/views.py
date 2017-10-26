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
from judge.oldcheck import bashoutput
from django.core.files.base import ContentFile
import threading
from datetime import datetime
from django.utils import timezone
from django.utils.six.moves.urllib.parse import urlencode
# Create your views here.
now = datetime.now()
def index(request):
	all_problems = Problem.objects.filter(contest__start_time__lte = timezone.now())
	return render(request,"problems/index.html", {'all_problems' : all_problems})

def problem(request, problemID):
	try:
		problem = Problem.objects.get(problem_ID=problemID)
	except Problem.DoesNotExist:
		raise Http404("There is no such problem. Please check again")
	if request.method == 'POST':
		#print("Hello World!!\n")
		submit_form = problems_forms.SubmitForm(request.POST, request.FILES)
		code_form = problems_forms.CodeForm(request.POST)
		test_form = problems_forms.TestForm(request.POST)
		print("\n")
		if submit_form.is_valid():
			#print("File submit")
			global last_queue
			last_queue = (last_queue + 1)%3
			submission = Submission()
			submission = submit_form.save(commit=False)
			submission.user = User.objects.get(username=request.user)
			submission.problem = problem
			submission.queue = Queue.objects.all()[last_queue]
			submission.save()
			messages.success(request, 'Successfully Submitted')
			if not grader_running[last_queue]:
				t = threading.Thread(target=grader,kwargs={'queue_number':last_queue})
				t.start()
			return redirect(reverse('mysubmissions', kwargs={'username':request.user}))
		elif code_form.is_valid():
			#print(2)
			#print("Ace code")
			def process():
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
			process()
			messages.success(request, 'Successfully Submitted')
			if not grader_running[last_queue]:
				t = threading.Thread(target=grader,kwargs={'queue_number':last_queue})
				t.start()
			return redirect(reverse('mysubmissions', kwargs={'username':request.user}))
		elif test_form.is_valid():
			#print("He doesnt terminal")
			data = test_form.cleaned_data
			test_lang = data['test_lang']
			test_code = data['test_code']
			test_input = data['test_input']
			username_of_user = request.user.username

			f = open("uploads/users/%s/test.%s"%(username_of_user,test_lang),"w+")
			f.write(test_code)
			f.close()
			g = open("uploads/users/%s/inp"%(username_of_user),"w+")
			g.write(test_input)
			g.close()
			output = bashoutput("uploads/users/%s/test.%s"%(username_of_user,test_lang),"uploads/users/%s/inp"%(username_of_user),test_lang)
			args = {}
			args.update(csrf(request))
			args['submit_form'] = problems_forms.SubmitForm()
			args['code_form'] = problems_forms.CodeForm()
			args['test_form'] = problems_forms.TestForm()
			args['problem'] = problem
			contest = problem.contest
			args['contest'] = contest
			args['output'] = "Output :\n" + output
			args['hide_or_not'] = "visible"
			args['text_on_ace'] = test_code
			args['lang_for_ace'] = test_lang
			if contest.end_time.strftime('%Y-%m-%d %H:%M') <= now.strftime('%Y-%m-%d %H:%M'):
				return render(request,"problems/problem.html", args)
			elif contest.start_time.strftime('%Y-%m-%d %H:%M') <= now.strftime('%Y-%m-%d %H:%M'):
				registered = contest.registered_user.filter(username = request.user.username)
				args['registered'] = registered
				return render(request,"problems/isactive.html", args)
			else:
				raise Http404("There is no such problem you prick, you can't hack the system the system hacks you -_- !!")
		else:
			messages.warning(request, 'There was an error. Please check!')
	args = {}
	args.update(csrf(request))
	args['submit_form'] = problems_forms.SubmitForm()
	args['code_form'] = problems_forms.CodeForm()
	args['test_form'] = problems_forms.TestForm()
	args['problem'] = problem
	contest = problem.contest
	args['contest'] = contest
	args['text_on_ace'] = ""
	args['output']=""
	args['lang_for_ace']="cpp"
	args['hide_or_not']= "hidden"
	if contest.end_time.strftime('%Y-%m-%d %H:%M:%S') <= timezone.make_aware(datetime.now(),timezone.get_default_timezone()).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'):
		return render(request,"problems/problem.html", args)
	elif timezone.make_aware(datetime.now(),timezone.get_default_timezone()).astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S') >= contest.start_time.strftime('%Y-%m-%d %H:%M:%S'):
		registered = contest.registered_user.filter(username = request.user.username)
		args['registered'] = registered
		return render(request,"problems/isactive.html", args)
	else:
		raise Http404("There is no such problem you prick, you can't hack the system the system hacks you -_- !!")
