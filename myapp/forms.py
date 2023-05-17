from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import PrivateMessage
from django.core.exceptions import ValidationError

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


    def clean_username(self):
        username = self.cleaned_data.get('username')
        min_length = 3
        if len(username) < min_length:
            raise ValidationError(f"Username must be at least {min_length} characters long.")
        return username

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )




class PrivateMessageForm(forms.ModelForm):
    class Meta:
        model = PrivateMessage
        fields = ['content']


