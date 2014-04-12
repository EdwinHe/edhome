from django import forms

class UploadFileForm(forms.Form):
    chosen_file  = forms.FileField()