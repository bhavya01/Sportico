from django.conf.urls import url
import django.contrib.auth.views
from . import views
from login.forms import LoginForm

urlpatterns = [
	url(r'^logout/$', django.contrib.auth.views.logout, {'next_page': '/login'}),
    url(r'^login/$', django.contrib.auth.views.login, {'template_name': 'login/login.html', 'authentication_form': LoginForm}),
    url(r'^register/$', views.register, name='register'), 
	url(r'^reason/$', views.reason, name='reason'),
	url(r'^privacy/$', views.privacy, name='privacy'),
    url(r'^terms/$', views.terms, name='terms'),
    url(r'^about/$', views.about, name='about')
]
