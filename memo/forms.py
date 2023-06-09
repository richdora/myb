from django import forms
from .models import Memo, Tag
from django_summernote.widgets import SummernoteWidget
import json


class MemoForm(forms.ModelForm):
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False}),
        required=False
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': False, 'placeholder': 'password(option)'}),
        required=False
    )



    class Meta:
        model = Memo
        fields = ['content', 'tags', 'password']


        widgets = {
            'content': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '180px'}, 'placeholder': ''}),
         }

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            tags = [tag["value"] for tag in json.loads(tags)]
            tag_objects = [Tag.objects.get_or_create(name=tag.strip())[0] for tag in tags]
            return tag_objects
        return []