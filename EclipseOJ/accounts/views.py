from django.shortcuts import render_to_response
from .forms import SignupForm
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    args = {}
    args.update(csrf(request))
    args['form'] = SignupForm()
    return render_to_response('accounts/signup.html', args)
