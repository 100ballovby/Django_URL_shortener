from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.user_signup, name='sign-up'),
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('account/', views.user_profile, name='account'),
]
