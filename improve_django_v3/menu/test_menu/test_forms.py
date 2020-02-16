from datetime import datetime

from django import forms
from django.test import SimpleTestCase, TestCase
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.contrib.auth.models import User
from django.utils import timezone

from ..forms import MenuForm
from ..models import Item, Ingredient, Menu

from ..form_utils import validate_season


class TestValidators(SimpleTestCase):
    '''Verify that the season for a given menu is
    exactly 'Summer', 'Fall', 'Winter', or 'Spring'.'''

    def test_validate_season_invalid_value(self):
        with self.assertRaisesMessage(
                ValidationError,
                '''Specify whether the menu falls within the Summer, Fall, Winter, or Spring.'''
        ):
            validate_season("January")

    def test_validate_season_valid_value(self):
        '''Validators return if they pass'''
        self.assertIsNone(None, validate_season('Spring'))


class TestMenuFields(TestCase):
    '''Validate that each field returns either cleaned data or raises a Validation Error'''

    def test_season_field(self):
        self.assertFieldOutput(
            forms.CharField,
            {'Dinner (Winter 2018)': 'Dinner (Winter 2018)'},
            {"October 20": ['Specify whether the menu falls within the Summer, Fall, Winter, or Spring.']},
            field_kwargs={'validators': [validate_season]}
        )

class TestMenuForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_chef = User.objects.create_user("test_chef")
        eggs = Ingredient.objects.create(name="Eggs")
        flour = Ingredient.objects.create(name="Flour")
        milk = Ingredient.objects.create(name="Milk")
        butter = Ingredient.objects.create(name="Butter")
        vanilla_extract = Ingredient.objects.create(name="Vanilla Extract")
        sugar = Ingredient.objects.create(name="Sugar")
        cls.item = Item.objects.create(
            name="Crepe",
            description="A thin pancake orginiating from France",
            chef=test_chef,
            created_date=timezone.now(),
            standard=True
        )
        cls.item.ingredients.add(eggs, flour, milk, butter, vanilla_extract, sugar,)# watch for potential error when running test
        cls.menu = Menu.objects.create(
            season="Fall"
        )
        cls.menu.items.add(cls.item)


class TestMenuExpirationAndCurrentDates(TestMenuForm):
    '''Validate that an error is raised when an
    expiration date is defined prior to the created date'''

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.data = {
            'season': 'Late Fall',
            'items': ['Crepe'],
            'expiration_date': datetime(2018, 1, 2)
        }

        cls.menu_form = MenuForm(cls.data)

    def test_menu_model_clean(self):
        self.assertTrue(
            self.menu_form.has_error(
                NON_FIELD_ERRORS, "invalid_expiration_date"
            )
        )

class TestMenuTitleAndExpirationDate(TestMenuForm):
    '''Validate that an error is raised when the menu's  
    title contains a year that is postdated relative 
    to its expiration date.'''

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.data = {
            'season': 'Late Fall 2021',
            'items': ['Crepe'],
            'expiration_date': datetime(2020, 3, 2)
        }

        cls.menu_form = MenuForm(cls.data)

    def test_menu_clean_expiration_date(self):
        self.assertTrue(
            self.menu_form.has_error(
                NON_FIELD_ERRORS, "post_date_error"
            )
        )