from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_countries import countries
from .models import *

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=70)
    country = forms.ChoiceField(countries)
    city = forms.CharField(max_length=100)
    institute = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', )

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None
        self.fields['username'].help_text = "Your username should contain only letters, numbers and symbols including _ @ . + -"    

    def save(self, commit=True):
        newuser = super(UserForm, self).save(commit=False)
        newuser.save()
        profile = Profile(user=newuser)
        profile.save()
        profile.email = self.cleaned_data["email"]
        profile.first_name = self.cleaned_data["first_name"]
        profile.last_name = self.cleaned_data["last_name"]
        profile.country = self.cleaned_data["country"]
        profile.city = self.cleaned_data["city"]
        profile.institute = self.cleaned_data["institute"]
        if commit:
            newuser.save()
        profile.save()
        return newuser

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    picture = forms.ImageField(label=('Profile Picture'),required=False, error_messages = {'Picture': ("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['country', 'institute', 'city', 'picture']
