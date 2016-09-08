from django import forms
from CMDB.models import *
from models import UploadFile

class DocumentForm(forms.Form):
    docfile = forms.FileField(
        label='Select a file'
    )
