from django import forms
from judge import models as judge_models

class SubmitForm(forms.ModelForm):
    class Meta:
        model = judge_models.Submission
        fields = ['language', 'uploaded_file']

class CodeForm(forms.Form):
    lang = forms.CharField(max_length=4)
    code = forms.CharField(widget=forms.Textarea)
