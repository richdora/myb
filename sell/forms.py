from django import forms
from .models import SellItem

class SellItemForm(forms.ModelForm):
    class Meta:
        model = SellItem
        fields = ['title', 'comment', 'photo1', 'photo2', 'photo3']
        widgets = {
            'photo1': forms.ClearableFileInput(attrs={'multiple': False}),
            'photo2': forms.ClearableFileInput(attrs={'multiple': False}),
            'photo3': forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def __init__(self, *args, **kwargs):
        super(SellItemForm, self).__init__(*args, **kwargs)
        self.fields['photo1'].label = "Photo 1"
        self.fields['photo2'].label = "Photo 2"
        self.fields['photo3'].label = "Photo 3"
