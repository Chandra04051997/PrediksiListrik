from django import forms
from .models import data, hasil, datasCSV

class FileForm(forms.ModelForm):
    class Meta:
        model = datasCSV
        fields = ('file',)
    