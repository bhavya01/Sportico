from django.shortcuts import render
from login.forms import UserForm
from django.contrib.auth import login
from login.models import *
from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

def reason(request):
	return render(request,"login/reason.html")

def privacy(request):
	return render(request,"login/privacy.html")

def terms(request):
	return render(request,"login/terms.html")

def about(request):
	return render(request,"login/about.html")

def register(request):
	success = False
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.set_password(user.password)
			user.communityRating = 1500
			user.appJoinDate = datetime.date.today()
			user.save()
			login(request,user)
			success = True
	else:
		form = UserForm()
	return render(request, 'login/register.html', {'form': form, 'success': success})