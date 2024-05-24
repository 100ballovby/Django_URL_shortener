from .models import Page


def menu(request):
	navigation = Page.objects.filter(active=True)
	return {'menu': navigation}


