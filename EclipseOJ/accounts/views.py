from django.shortcuts import render_to_response
from . import forms as accounts_forms
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse

def signup(request):
    if request.method == 'POST':
        user_form = accounts_forms.UserForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            #messages.success(request, _('Your profile was successfully updated!'))
            login(request, new_user)
            return redirect(reverse('homepage'))
    args = {}
    args.update(csrf(request))
    args['user_form'] = accounts_forms.UserForm()
    return render_to_response('accounts/signup.html', args)
