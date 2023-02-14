from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.db import models
from django.forms import ModelForm
from .models import RequesterModel,DonnerModel
# Create your forms here.

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(UserRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user



class RequesterForm(ModelForm):
	class Meta:
		model = RequesterModel 
		fields = ['fullname','Rid','phone_no','is_diabitic','BloodGrp','Age','city','state']


class DonnerForm(ModelForm):
	class Meta:
		model = DonnerModel 
		fields = ['fullname','Did','phone_no','is_diabitic','BloodGrp','Age','city','state','Bid']
