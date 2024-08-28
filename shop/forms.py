from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))


class RegisterForm(UserCreationForm):

    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }))


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')


