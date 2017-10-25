from django.shortcuts import render, redirect, get_object_or_404
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
from django.http import JsonResponse


def signup(request):
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
    args = {}
    args.update(csrf(request))
    args['user_form'] = UserForm()
    return render(request, 'core/signup.html', args)

def home(request):
    if request.user.is_authenticated():
        return redirect('/profile/')
    return render(request, 'core/home.html')

def profile(request):
    return redirect('other_profile', username=request.user.username)

def other_profile(request, username):
    try:
        user = User.objects.filter(Q(is_superuser=False)).get(username=username)
    except User.DoesNotExist:
        return render(request, 'warning.html', {'warning': 'No such user found. Please verify.'})
    return render(request, 'core/detail.html', {'user': user})

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
# def change_password(request):
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  # Important!
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('/contests')
#         else:
#             messages.error(request, 'Please correct the error(s) below.')
#     else:
#         form = PasswordChangeForm(request.user)
#     return render(request, 'profiles/change_password.html', {
#         'form': form
#     })
