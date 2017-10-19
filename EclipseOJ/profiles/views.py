from django.shortcuts import render, render_to_response, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.http import Http404
from . import forms as profiles_forms
from django.template.context_processors import csrf
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView
from accounts.models import Profile
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User, Permission
from django.db.models import Q
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm

def index(request):
    #return HttpResponse("<h1>Yo i'll probably put list of users here</h1>")
    all_users = User.objects.filter(Q(is_superuser=False))
    #template = loader.get_template('profiles/index.html') no bro we'll use shortcut
    context = {'all_users': all_users }  #context is a dictionary here!!!
    return render(request, 'profiles/index.html', context)

def detail(request,nickname):
    #return HttpResponse("<p>I have to display about user " + str(nickname) + "</p>")
    try:
        user = User.objects.filter(Q(is_superuser=False)).get(username=nickname)
    except User.DoesNotExist:
        raise Http404("There is no such username :/ Please check again :P")
    if user == request.user:
        return render(request, 'profiles/self_detail.html', { 'user': user })
    else:
        return render(request, 'profiles/other_detail.html', { 'user': user })

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'profiles/change_password.html', {
        'form': form
    })

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    #context_object_name = 'variable_used_in `profiles/update.html`'
    model = Profile
    form_class = profiles_forms.ProfileUpdateForm
    template_name = 'profiles/update.html'
    success_url = '/contests/'
    success_message = 'Updated Succesfully'

    def get_initial(self):
        initial = super(ProfileUpdateView, self).get_initial()
        #print('initial data', initial)
        habit_object = self.get_object()
        initial['city'] = habit_object.city
        initial['country'] = habit_object.country
        initial['institute'] = habit_object.institute
        return initial

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user=self.request.user)
#
# @login_required
# class UserUpdateView(UpdateView):
#     model = User
#     fields = ('first_name', 'last_name', 'email')
#     template_name = 'profiles/update.html'
#
# @login_required
# def update(request):
#     if request.method == 'POST':
#         profile_update_form = profiles_forms.ProfileUpdateForm(request.POST, instance=request.user)
#         user_update_form = profiles_forms.UserUpdateForm(request.POST, instance=request.user.profile)
#         if user_update_form.is_valid() and profile_update_form.is_valid():
#             update_form.save()
#             profile_update_form.save()
#             #messages.success(request, _('Your profile was successfully updated!'))
#             return redirect(reverse('index'))
#     args = {}
#     args.update(csrf(request))
#     args['user_update_form'] = profiles_forms.UserUpdateForm()
#     args['profile_update_form'] = profiles_forms.ProfileUpdateForm()
#     return render_to_response('profiles/update.html', args)
