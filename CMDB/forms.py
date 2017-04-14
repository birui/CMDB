from django import forms
from CMDB.models import *
from models import UploadFile

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )

class NameForm(forms.Form):
    your_name = forms.CharField(label='Your name', max_length=100)
    email = forms.EmailField()
    url = forms.URLField()
    