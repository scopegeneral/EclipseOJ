from django import forms
from judge import models as judge_models

class SubmitForm(forms.ModelForm):
    """
    This form is for submission of programming files on the system. It's a ModelForm i.e. it instantiates the Submission object
    """
    class Meta:
        model = judge_models.Submission
        fields = ['language', 'uploaded_file']

class CodeForm(forms.Form):
    """
    This is used for submitting solution on the website through ace text editor. We have used hidden fields and subsequently created editor interface
    """
    lang = forms.CharField(max_length=4,widget=forms.HiddenInput)
    code = forms.CharField(widget=forms.HiddenInput)

class TestForm(forms.Form):
    """
    This is used for testing solution on the website through ace text editor. We have used hidden fields and subsequently created editor interface
    """
    test_lang = forms.CharField(max_length=4,widget=forms.HiddenInput)
    test_code = forms.CharField(widget=forms.HiddenInput)
    test_input = forms.CharField(max_length=800,widget=forms.HiddenInput,required=False)
