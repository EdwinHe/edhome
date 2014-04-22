from django import forms

from ozio.models import *

form_style = 'form-control input-sm'

class UploadFileForm(forms.Form):
    chosen_file  = forms.FileField()

        
class TypeForm(forms.ModelForm):
    class Meta:
        model = Type    
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(TypeForm, self).__init__(*args, **kwargs)
        for f in self.fields.keys():
            self.fields[f].widget.attrs.update({'class' : form_style})
        
        
class CateForm(forms.ModelForm):
    class Meta:
        model = Cate    
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(CateForm, self).__init__(*args, **kwargs)
        for f in self.fields.keys():
            self.fields[f].widget.attrs.update({'class' : form_style})

class SubCateForm(forms.ModelForm):
    class Meta:
        model = SubCate    
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(SubCateForm, self).__init__(*args, **kwargs)
        for f in self.fields.keys():
            self.fields[f].widget.attrs.update({'class' : form_style})
        
class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword    
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(KeywordForm, self).__init__(*args, **kwargs)
        for f in self.fields.keys():
            self.fields[f].widget.attrs.update({'class' : form_style})
        
        
class SourceFileForm(forms.ModelForm):
    class Meta:
        model = SourceFile    
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(SourceFileForm, self).__init__(*args, **kwargs)
        for f in self.fields.keys():
            self.fields[f].widget.attrs.update({'class' : form_style})

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction    
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        for f in self.fields.keys():
            self.fields[f].widget.attrs.update({'class' : form_style})

        
class TransactionFilterForm(forms.ModelForm):
    class Meta:
        model = TransactionFilter    
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(TransactionFilterForm, self).__init__(*args, **kwargs)
        for f in self.fields.keys():
            self.fields[f].widget.attrs.update({'class' : form_style})
        
class FilterSQLForm(forms.ModelForm):
    class Meta:
        model = FilterSQL
        # exclude = [] # uncomment this line and specify any field to exclude it from the form

    def __init__(self, *args, **kwargs):
        super(FilterSQLForm, self).__init__(*args, **kwargs)
        for f in self.fields.keys():
            self.fields[f].widget.attrs.update({'class' : form_style})