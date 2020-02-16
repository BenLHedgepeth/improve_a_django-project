from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from datetime import datetime

from ..models import Ingredient, Item, Menu

class TestMenuView(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username="Masterchef",
            password="secret"
        )

        cls.butter = Ingredient.objects.create(name="Butter")
        cls.egg = Ingredient.objects.create(name="Egg")

        cls.scrambled_eggs = Item.objects.create(
            name="Scrambled Eggs",
            description="English-style eggs",
            chef=cls.test_user,
            created_date=datetime.now(),
            standard=True
        )
        cls.scrambled_eggs.ingredients.add(cls.egg, cls.butter)

        cls.menu = Menu.objects.create(
            season="Late Spring 2018",
            created_date=datetime.now()
        )

        cls.menu.items.add(cls.scrambled_eggs)


class TestNewMenuAdded(TestMenuView):
    '''Verify that a chef has added anew menu'''

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.menu_data = {
            'season': 'Summer 2020',
            'items': ['Scrambled Eggs'],
            'expiration_date': datetime(year=2020, month=7, day=4)
        }

    def test_create_new_menu_added(self):
        self.client.force_login(self.test_user)
        response = self.client.post(
          reverse("menu:menu_new"),
          data=self.menu_data,
          follow=True
        )
        self.assertTemplateUsed('menu/menu_detail.html')
        self.assertContains(response, "Menu added: Summer 2020")


class TestEditExistingMenu(TestMenuView):
    '''Verify that an existing menu's attributes
    are updated when a user changes changes
    selected fields in the MenuForm'''

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        flour = Ingredient.objects.create(name="Flour")
        milk = Ingredient.objects.create(name="Milk")
        vanilla_extract = Ingredient.objects.create(name="Vanilla Extract")
        sugar = Ingredient.objects.create(name="Sugar")
        cls.crepe = Item.objects.create(
            name="Crepe",
            description="A thin pancake orginiating from France",
            chef=cls.test_user,
            created_date=datetime.now(),
            standard=True
        )
        cls.crepe.ingredients.add(cls.egg, cls.butter, flour, milk, vanilla_extract, sugar,)

        cls.updated_attrs = {
            'season': "Late Spring 2018",
            'items': ['Crepe', 'Scrambled Eggs'],
        }


    def test_menu_instance_items_updated(self):
        self.client.force_login(self.test_user)
        response = self.client.post(
            reverse("menu:menu_edit", kwargs={'pk': 1}),
            data=self.updated_attrs,
            follow=True
        )
        self.assertRedirects(
            response, reverse("menu:menu_detail", kwargs={'pk': 1})
        )
        self.assertTemplateUsed("menu/menu_detail.html")
        self.assertContains(response, "Menu is up to date!")



class TestMenuListingView(TestCase):
    '''Verify that'''
    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username="Masterchef",
            password="Secret"
        )
    
    def test_get_menu_list_logged_in(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse("menu:menu_list")
        )
        self.assertTemplateUsed('menu/list_all_curreent_menus.html')
        self.assertContains(response, "Log Out")

    def test_get_menu_list_logged_out(self):
        response = self.client.get(
            reverse("menu:menu_list")
        )
        self.assertTemplateUsed('menu/list_all_curreent_menus.html')
        self.assertContains(response, "Log In")