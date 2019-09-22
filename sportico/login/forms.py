from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from django.core.validators import validate_email
from django.contrib.auth import get_user_model
from login.choices import *

User = get_user_model()

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))

class UserForm(ModelForm):
	username = forms.CharField(label="Choose your username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username', 'placeholder': 'UserName'}))
	first_name = forms.CharField(label="Name", max_length=30, required = True,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name', 'placeholder': 'First'}))
	last_name = forms.CharField(label="Name", max_length=30, required = False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name', 'placeholder': 'Last'}))
	street = forms.CharField(label="Address", max_length=30, required = False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'street', 'placeholder': 'Street'}))
	city = forms.CharField(label="Address", max_length=30, required = False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'city', 'placeholder': 'City'}))
	state = forms.CharField(label="Location", max_length=30, required = False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'state', 'placeholder': 'State'}))
	country = forms.CharField(label="Location", max_length=30, required = False,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'country', 'placeholder': 'Country'}))
	phoneNumber = forms.CharField(label="Phone Number", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'phoneNumber'}))
	email = forms.EmailField(label="Email", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'email'}))
	password = forms.CharField(label="Create a password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))
	confirm_password = forms.CharField(label="Confirm your password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'confirm_password'}))
	gender = forms.ChoiceField(
        required=False,
        widget=forms.Select,
        choices=GENDER_CHOICES,
    )

	birthDate = forms.DateField(
		label="Birth Date",
	    widget=forms.SelectDateWidget(years=BIRTH_YEAR_CHOICES,
	        empty_label=("Choose Year", "Choose Month", "Choose Day"),
	    ),
	)

	def clean(self): 
		if 'password' in self.cleaned_data and 'confirm_password' in self.cleaned_data:
			if self.cleaned_data['password'] != self.cleaned_data['confirm_password']: 
				raise forms.ValidationError(_("Passwords do not match each other"))

		if User.objects.filter(username=self.cleaned_data['username']).exists():
			raise forms.ValidationError(_("Username is already used"))

		if User.objects.filter(email=self.cleaned_data['email']).exists():
			raise forms.ValidationError(_("Email Address is already used"))

		return self.cleaned_data

	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'street', 'city', 'state', 'country', 'phoneNumber', 'email', 'password', 'confirm_password', 'gender', 'birthDate')