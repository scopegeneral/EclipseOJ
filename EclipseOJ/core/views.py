from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.models import User
from django.template.context_processors import csrf
from django.views.generic import UpdateView
from django.contrib.auth import login
from django.contrib import messages
from .forms import *
from .models import *
from django.db.models import Q
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect


def signup(request):
    """
    This is basically a django form view for registering into the website and creating profile of user.
    All relevant fields related to profile are set up by the user.


    **Template:**
    :template:`core/signup.html`

    """
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save()
            login(request, new_user)
            messages.success(request, 'Signup successful!')
            next = request.POST.get('next', '/')
            return redirect(next)
        else:
            for form_error in user_form.errors:
                for e in user_form.errors[form_error].as_data():
                    if (form_error == 'password2'):
                        messages.error(request, str(e)[2:-2])
                    else:
                        messages.error(request, '{}: {}'.format(form_error, str(e)[2:-2]))
    if request.user.is_authenticated():
        return redirect('contests_index')
    args = {}
    args.update(csrf(request))
    args['user_form'] = UserForm()
    return render(request, 'core/signup.html', args)

def logged_in_message(sender, user, request, **kwargs):
    messages.success(request, "Welcome {}!".format(user.username))

user_logged_in.connect(logged_in_message)

def home(request):
    """
    This is the homepage of our website. For users not logged in this is set to homepage containing links to signup and login forms and set to profile view for logged in users.

    **Template:**

    :template:`core/profile.html`
    :template:`core/home.html`
    """
    if request.user.is_authenticated():
        return redirect('/profile/')
    return render(request, 'core/home.html')

def profile(request):
    """
    This is the profile view of users. This further either redirects to other_profile view or the login view.
    """
    if request.user.is_authenticated():
        return redirect('other_profile', username=request.user.username)
    else:
        return HttpResponseRedirect(reverse('login') + "?{}".format(request.path))

def other_profile(request, username):
    """
    This view is the detailed view of user. It shows all details about a particular user. Any valid regex matching the URL pattern allows you to see the profile of user. If the request.user is the one whose profile has been visited then it allows to edit details through update profile link.

    **Template:**

    :template:`core/detail.html`
    """
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return render(request, 'warning.html', {'warning': 'No such user found. Please verify.'})
    if user.is_superuser:
        return redirect('contests_index')
    return render(request, 'core/detail.html', {'user': user})

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    This is the update profile option for user, where user can update his old setting and change them. He can change his city, country, institute, and profile picture.
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'core/update.html'
    success_message = 'Updated Succesfully'

    def get_success_url(self):
        return self.request.POST.get('next', '/profile')

    def get_initial(self):
        initial = super(ProfileUpdateView, self).get_initial()
        habit_object = self.get_object()
        initial['city'] = habit_object.city
        initial['country'] = habit_object.country
        initial['institute'] = habit_object.institute
        initial['picture'] = habit_object.picture
        return initial

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, user=self.request.user)


def validate_username(request):
    """
    This view is used in the dynamic asynchronous AJAX verification of username in the signup form.
    When user types in the username and shifts focus from the usernamr box, a post request is created which calls this view and checks whether the username is available or not.
    This views is a JSONdata file consisting of usernames
    """
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
