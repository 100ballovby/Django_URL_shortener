from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
	model = User
	fields = ['username', 'email', 'password1',
	          'password2', 'first_name', 'last_name']


class LoginForm(forms.Form):
	username_or_email = forms.CharField(widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder': 'Имя пользователя или Email'}
	))
	password = forms.CharField(widget=forms.PasswordInput(
		attrs={'class': 'form-control', 'placeholder': 'Пароль'}
	))

