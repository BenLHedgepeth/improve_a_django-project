from django.test import TestCase
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ..forms import ChefRegisterationForm, ChefAuthenticationForm
from ..validators import validate_username


class TestUsernameValidator(TestCase):
    '''Verify that the custom validator `validate_username`
    raises a ValidationError when certain characters are
    included in a username'''

    def test_validate_username_fail(self):
        with self.assertRaisesMessage(ValidationError, "Username must only contain characters: [A-Z; a-z, 0-9, _]"):
            validate_username("+Chef*Amazing")

    def test_validate_username_success(self):
        self.assertIsNone(validate_username("test_chef"))


class TestChefRegisterationForm(TestCase):
    '''Verify the username field's cleaned data and its 
    validation errors in the event of an valid/invalid 
    username.'''

    @classmethod
    def setUpTestData(cls):
        cls.field_inputs = {
            'valid': 'test_chef',
            'invalid': 'test*#-chef'
        }

    def test_chef_registeration_username_field_valid(self):
        self.assertFieldOutput(
            forms.CharField,
            {'test_chef': 'test_chef'},
            {'test(#-Chef': ["Username must only contain characters: [A-Z; a-z, 0-9, _]"]},
            field_kwargs={'validators': [validate_username]}
        )
    

class TestChefAuthenticationForm(TestCase):
    '''Verify that ChefAuthenticationForm cleans the
    username. A ValidationError is expected to be raised;
    no User exists with the username supplied in the form 
    submission. Attempting to login will fail.'''

    @classmethod
    def setUpTestData(cls):
        login_data = {
            'username': 'Masterchef',
            'password': 'password'
        }

        cls.test_authenticate_form = ChefAuthenticationForm(data=login_data)

    def test_clean_username_does_not_exist(self):
        self.assertTrue(
            self.test_authenticate_form.has_error('username', 'no_user_exists')
        )


class TestChefAuthenicationForm_Case2(TestCase):
    '''Verify that ChefAuthenticationForm cleans the
    username. No ValidationError is raised due to an
    User existing in the database with a given username.'''

    @classmethod
    def setUpTestData(cls):
        User.objects.create(
            username="Masterchef",
            password="password"
        )
        login_data = {
            'username': 'Masterchef',
            'password': 'password'
        }

        '''Keyword argument for `data` must be supplied. AuthenticationForm
        expects `request` as its first argument, but it's default value is
        set to None'''

        '''https://github.com/django/django/blob
        /master/django/contrib/auth/forms.py#L172'''

        cls.authentication_form = ChefAuthenticationForm(data=login_data)

    def test_clean_username_exists(self):
        self.assertFalse(
            self.authentication_form.has_error('username', 'no_user_exists')
        )


class TestChefAuthenticationFormWidgets(TestCase):
    '''Verify that each form field in the Login Form
    has a CSS class attribute defined "text_widget"'''

    @classmethod
    def setUpTestData(cls):
        login_data = {
            'username': 'Masterchef',
            'password': 'password'
        }
        cls.login_form = ChefAuthenticationForm(data=login_data)
        cls.username_field_widget = cls.login_form.fields['username'].widget.attrs
        cls.password_field_widget = cls.login_form.fields['password'].widget.attrs

    def test_chef_authencation_form_field_css_class(self):
        print(self.login_form.as_p())
        self.assertIn('class', self.username_field_widget)
        self.assertIn('class', self.password_field_widget)