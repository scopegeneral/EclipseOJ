from django import forms

class SearchForm(forms.Form):
    userID = forms.CharField(label='username', max_length=100, required=False)
    countryID = forms.CharField(label='country', max_length=100, required=False)
    cityID = forms.CharField(label='city', max_length=100, required=False)
    instiID = forms.CharField(label='institute', max_length=100, required=False)
