from django import forms
from django.contrib.auth.models import User
from accounts.models import Profile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    picture = forms.ImageField(label=('Profile Picture'),required=False, error_messages = {'invalid': ("Image files only")}, widget=forms.FileInput)
    class Meta:
        model = Profile
        fields = ['country', 'institute', 'city', 'picture']
