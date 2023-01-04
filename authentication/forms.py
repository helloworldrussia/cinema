from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from authentication.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email',)


# class SignInForm(AuthenticationForm):
#     username = forms.EmailField(label='Email', widget=forms.EmailInput)
#     password = forms.CharField(label='Password', widget=forms.PasswordInput)
