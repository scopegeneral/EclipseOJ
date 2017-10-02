from django.shortcuts import render_to_response
from . import forms as accounts_forms
from django.template.context_processors import csrf
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages

def signup(request):
    if request.method == 'POST':
        user_form = accounts_forms.UserForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            login(request, new_user)
            messages.success(request, 'Signup successful!')
            return redirect(reverse('homepage'))
        else:
            messages.warning(request, 'There was an error. Please check your details!')
    args = {}
    args.update(csrf(request))
    args['user_form'] = accounts_forms.UserForm()
    return render(request, 'accounts/signup.html', args)
