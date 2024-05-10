from django.shortcuts import render, redirect
from .models import Links, Clicks
from .forms import CreateUrlForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import hashlib
import string
# Create your views here.


def redirect_url(request, short_url):
	print(short_url)
	try:
		url = Links.objects.get(short_url=short_url)
	except Links.DoesNotExist:
		return render(request, '404.html')
	url.clicks_qty += 1  # засчитываем один клик при переходе по ссылке
	url.save()  # применить изменения в БД
	click = Clicks(
		link_id=url,
	    ip_address=request.META['REMOTE_ADDR'],
		user_agent=request.META['HTTP_USER_AGENT']
	)
	click.save()
	return redirect(url.original_url)


#@login_required
def create_short_link(request):
	form = CreateUrlForm(request.POST)
	user = request.user
	if form.is_valid():
		name = form.cleaned_data['name']
		or_url = form.cleaned_data['original_url']
		s_link = generate_short_url(str(user), or_url)
		new_url = Links(
			name=name,
			user=User.objects.first(),
			original_url=or_url,
			short_url=s_link,
		)
		new_url.save()
		return redirect('create-link')
	return render(request, 'create-link.html', {'form': form})


def generate_short_url(username, full_url):
	# сгенерируем хеш из имени пользователя и оригинальной ссылки
	hash_str = hashlib.sha256((username + full_url).encode('utf-8')).hexdigest()
	# преобразуем хеш в base64, чтобы сделать ссылку короткой
	short_url = ''
	char_pool = string.digits + string.ascii_letters
	for i in range(7):
		index = int(hash_str[i * 2:i * 2 + 2], 16) % len(char_pool)
		short_url += char_pool[index]

	return short_url


