from django import forms
from judge import models as judge_models

class SubmitForm(forms.ModelForm):
    class Meta:
        model = judge_models.Submission
        fields = ['language', 'uploaded_file']
