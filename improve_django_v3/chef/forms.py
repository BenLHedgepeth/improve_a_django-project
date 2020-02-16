from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .validators import validate_username
from django.forms.widgets import TextInput

class ChefRegisterationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = "form_text_widget"
            field.widget.attrs['placeholder'] = field.label

    username = forms.CharField(label="Username", validators=[validate_username]) # check for coverage
    password2 = forms.CharField( # check for coverage
        label="Verify Password",
        widget=forms.PasswordInput,
        error_messages={
            'required': "Provide a password"
        }
    )

    def clean(self):
        cleaned_data = super().clean()
        submitted_username = cleaned_data.get('username')
        submitted_password = cleaned_data.get('password1')
        
        if submitted_username == submitted_password:
            '''This error will be propogated to NON_FIELD_ERRORS'''
            raise ValidationError(
                "Your password cannot be your username.", code="invalid_password"
            )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']



class ChefAuthenticationForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for label, field in self.fields.items():
            field.widget.attrs['class'] = "form_text_widget"
            field.widget.attrs['placeholder'] = label.title()

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
