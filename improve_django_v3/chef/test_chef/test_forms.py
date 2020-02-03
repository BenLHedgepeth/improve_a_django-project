from django.test import TestCase
from django import forms
from django.core.exceptions import ValidationError
from ..forms import ChefRegisterationForm
from ..validators import validate_username


class TestUsernameValidator(TestCase):
    def test_validate_username_fail(self):
        with self.assertRaisesMessage(ValidationError, "Username must only contain characters: [A-Z; a-z, 0-9, _]"):
            validate_username("+Chef*Amazing")

    def test_validate_username_success(self):
        self.assertIsNone(validate_username("test_chef"))


class TestChefRegisterationForm(TestCase):

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
    