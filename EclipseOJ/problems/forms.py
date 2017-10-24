from django import forms
from judge import models as judge_models

class SubmitForm(forms.ModelForm):
    class Meta:
        model = judge_models.Submission
        fields = ['language', 'uploaded_file']

class CodeForm(forms.Form):
    lang = forms.CharField(max_length=4,widget=forms.HiddenInput)
    code = forms.CharField(widget=forms.HiddenInput)

class TestForm(forms.Form):
    test_lang = forms.CharField(max_length=4,widget=forms.HiddenInput)
    test_code = forms.CharField(widget=forms.HiddenInput)
    test_input = forms.CharField(max_length=800,widget=forms.HiddenInput,required=False)
