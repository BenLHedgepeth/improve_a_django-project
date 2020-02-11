from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .validators import validate_username
from django.forms.widgets import TextInput

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



class ChefAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        for label, field in self.fields.items():
            field.widget.attrs['class'] = "form_text_widget" 

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            site_user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError(
                """No account exists with that username. 
                Please create an account.""", code="no_user_exists"
            )
        return username

    class Meta:
        model = User
        fields = ['username', 'password']
