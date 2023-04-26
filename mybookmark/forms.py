from django import forms
from .models import Bookmark

class BookmarkForm(forms.ModelForm):
    youtube_link = forms.URLField(
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    comments = forms.CharField(  # Add this block
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Bookmark
        fields = ['youtube_link', 'comments']  # Update this line
