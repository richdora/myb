from django import forms
from .models import Photo, Tag
import json

class PhotoUploadForm(forms.ModelForm):
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False}),
        required=False
    )

    class Meta:
        model = Photo
        fields = ['image', 'comment', 'tags']

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'required': False}),
        }

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            tags = [tag["value"] for tag in json.loads(tags)]
            tag_objects = [Tag.objects.get_or_create(name=tag.strip())[0] for tag in tags]
            return tag_objects
        return []
