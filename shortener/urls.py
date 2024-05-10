from django.urls import path
from .views import redirect_url, create_short_link


urlpatterns = [
	path('<str:short_url>', redirect_url, name='redirect_url'),
	path('create-link/', create_short_link, name='create-link'),
]
