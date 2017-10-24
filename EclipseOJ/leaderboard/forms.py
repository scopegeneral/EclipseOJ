from django import forms

class SearchForm(forms.Form):
    userID = forms.CharField(label='Username', max_length=100, required=False)
    countryID = forms.CharField(label='Country', max_length=100, required=False)
    cityID = forms.CharField(label='City', max_length=100, required=False)
    instiID = forms.CharField(label='Institute', max_length=100, required=False)
