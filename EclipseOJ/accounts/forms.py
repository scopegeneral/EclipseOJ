from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django_countries import countries
from . import models as accounts_models

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=70)
    city = forms.CharField(max_length=100)
    country = forms.ChoiceField(countries)
    institute = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username',)

    def save(self, commit=True):
        newuser = super(UserForm, self).save(commit=False)
        newuser.save()
        profile = accounts_models.Profile(user=newuser)
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
