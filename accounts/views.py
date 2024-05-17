from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from shortener.models import Links, Clicks


# Create your views here.
def user_signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			password = form.cleaned_data.get('password1')
			user_instance = form.save()  # создаю экземпляр User с данными из формы
			messages.success(request, 'Регистрация прошла успешно!')
			return redirect('login')
		else:
			messages.error(request, 'Что-то пошло не так, попробуйте еще раз!')
	else:
		form = SignUpForm()
	return render(request, 'registration/register.html', {'form': form})


def user_logout(request):
	logout(request)
	return redirect('login')


def user_login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username_or_email = form.cleaned_data.get('username_or_email')
			password = form.cleaned_data.get('password')
			user = authenticate(request, username=username_or_email, password=password)
			if user is None:
				try:
					user = User.objects.filter(email=username_or_email).first()
					if user is not None:
						user = authenticate(request, username=user.username, password=password)
				except:
					messages.error(request, 'Неправильный логин и/или пароль')
					return redirect('login')
			if user:
				login(request, user)
				messages.success(request, 'Успешный вход!')
				return redirect('account')
			else:
				messages.error(request, 'Неверный логин и/или пароль')
				return redirect('login')
	else:
		form = LoginForm()
	return render(request, 'registration/login.html', {'form': form})


def user_profile(request):
	try:
		instance = User.objects.get(id=request.user.id)
		links = Links.objects.filter(user=instance)
		return render(request, 'registration/account.html', {'links': links})
	except:
		messages.error(request, 'Вы не вошли на сайт!')
		return redirect('login')
