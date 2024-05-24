from django.shortcuts import render
from .models import Page, Text


# Create your views here.
def page_view(request, url, child_url=None):
	try:
		page = Page.objects.get(url=child_url)  # из базы данных достать объект страницы, где поле url совпадает с запрошенным url
		text = Text.objects.filter(page_id=page.id).first()  # достаю текст, привязанный к найденной странице
	except:
		page = Page.objects.get(url=url)
		text = Text.objects.filter(page_id=page.id).first()
	return render(request, 'content/page.html', {'page': page, 'text': text})
