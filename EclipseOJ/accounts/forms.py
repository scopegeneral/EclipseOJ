from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models as accounts_models

class ProfileForm(forms.ModelForm):
    class Meta:
        model = accounts_models.Profile
        fields = ('country', 'institute', 'city')

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')

    def save(self, commit=True):
        newuser = super(UserForm, self).save(commit=False)
        newuser.email = self.cleaned_data["email"]
        newuser.first_name = self.cleaned_data["first_name"]
        newuser.last_name = self.cleaned_data["last_name"]
        if commit:
            newuser.save()
        return newuser
