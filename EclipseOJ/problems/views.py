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
	"""
    Display list of all :model:`problems.Problem` objects.

    This view enables the user to access all problems the problems from single page.

	**Args:**

    1. ``all_problems``
            It is a query-set of :model:`problems.Problem` constisting of all problems in the database

    **Template:**

    :template:`problems/index.html`
    """
	all_problems = Problem.objects.filter(contest__start_time__lte = timezone.now())
	return render(request,"problems/index.html", {'all_problems' : all_problems})

def problem(request, problemID):
	"""
    It is the detailed view for a particular problem.  This views enables you to access all problems in a particular contests. It has been divided into three parts and three different templates have been created for each of them

    1. Problem belonging to Past contests
    2. Problem belonging to Present contests

	The details of these views are as follows

	- If a user tries to access a problem which is stored in database but as a problem belong to future contest a 404 error page is displayed
	- For a user solving problem belonging to a past contest, he can submit his solution and get verdict on his solution. To submit his solution either he can attempt the problem on the inbuilt editor provided on the website which supports syntax highightening of multiple languages and submit or he can directly submit solution from his system. He can also run solution against custom input and get to know wether his solution is working as expected or not (when he is using the inbuilt editor)
	- For a current contest, if the user registered for the contest then he can access problems from the website. Apart from normal problem view, we have provided a countdown timer on website.

	**Args:**

    1. ``submit_form``
            It's a django form instance of SubmitForm
    2. ``code_form``
            It's a django form instance of CodeForm
	3. ``test_form``
            It's a django form instance of TestForm
	4. ``problem``
            It's an instance of the :model:`problems.Problem` object
	5. ``contest``
			It's an instance of the :model:`problems.Problem` object	6. ``text_on_ace``
	6. ``text_on_ace``
			It's the default text that appears on the ace editor
	7. ``lang_for_ace``
			It's the default language that appears in the ace editor
	8. ``output``
			It's the verdict which user gets when he tests code against custom input
	9. ``hide_or_not``
			It tells wether to show to output cardboard or not

	**Template:**

    1. :template:`contests/notactive.html`
    2. :template:`contests/contest.html`
    """
	try:
		problem = Problem.objects.get(problem_ID=problemID)
	except Problem.DoesNotExist:
		raise Http404("There is no such problem. Please check again")
	if request.method == 'POST':
		#print("Hello World!!\n")
		submit_form = problems_forms.SubmitForm(request.POST, request.FILES)
		code_form = problems_forms.CodeForm(request.POST)
		test_form = problems_forms.TestForm(request.POST)
		#print("\n")
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
