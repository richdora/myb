from django import forms
from .models import Photo, Tag
import json
from django_summernote.widgets import SummernoteWidget
from .models import Photo, RANGE_CHOICES

class PhotoUploadForm(forms.ModelForm):
    tags = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'required': False}),
        required=False
    )

    range = forms.ChoiceField(
        choices=RANGE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Photo
        fields = ['image', 'comment', 'tags', 'enable_secrets', 'range', 'secrets', ]

        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'required': False}),
            'secrets': SummernoteWidget(attrs={'summernote': {'width': '100%', 'height': '180px'}, 'placeholder': ''}),

        }

    def clean_tags(self):
        tags = self.cleaned_data.get('tags')
        if tags:
            tags = [tag["value"] for tag in json.loads(tags)]
            tag_objects = [Tag.objects.get_or_create(name=tag.strip())[0] for tag in tags]
            return tag_objects
        return []
