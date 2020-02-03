from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .validators import validate_username

class ChefRegisterationForm(UserCreationForm):

	username = forms.CharField(validators=[validate_username])

	def clean(self):
		cleaned_data = super().clean()
		submitted_username = cleaned_data.get('username')
		submitted_password = cleaned_data.get('password1')
		
		if submitted_username == submitted_password:
			raise ValidationError(
				"Your password cannot be your username.", code="invalid_password"
			)

	class Meta:
		model = User
		fields = ['username', 'password1', 'password2']
