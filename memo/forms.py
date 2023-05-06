from django import forms
from .models import Memo
from django_summernote.widgets import SummernoteWidget

class MemoForm(forms.ModelForm):

    class Meta:
        model = Memo
        fields = ['title', 'content',]


        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',}),
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '180px'}, 'placeholder': ''}),
         }
