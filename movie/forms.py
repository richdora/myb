from django import forms
from .models import Movie, Tag
import json


class MovieForm(forms.ModelForm):
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False}),
        required=False
    )

    class Meta:
        model = Movie
        fields = ['youtube_link', 'comments', 'tags']

        widgets = {
            'youtube_link': forms.URLInput(attrs={'class': 'form-control'}),
            'comments': forms.Textarea(attrs={'class': 'form-control', 'required': False}),
        }

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            tags = [tag["value"] for tag in json.loads(tags)]
            tag_objects = [Tag.objects.get_or_create(name=tag.strip())[0] for tag in tags]
            return tag_objects
        return []
