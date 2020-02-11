from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.urls import reverse
from datetime import datetime

from ..models import Ingredient, Item


class TestNewMenuAdded(TestCase):
    '''Verify that a chef has added a
    new menu'''

    @classmethod
    def setUpTestData(cls):
        cls.test_user = User.objects.create_user(
            username="Masterchef",
            password="secret"
        )
        cls.menu_data = {
            'season': 'Summer 2020',
            'items': ['Scrambled Eggs'],
            'expiration_date': datetime(year=2020, month=7, day=4)
        }

        butter = Ingredient.objects.create(name="butter")
        egg = Ingredient.objects.create(name="egg")

        scrambled_eggs = Item.objects.create(
            name="Scrambled Eggs",
            description="English-style eggs",
            chef=cls.test_user,
            created_date=datetime.now(),
            standard=True
        )
        scrambled_eggs.ingredients.add(egg, butter)


    def test_create_new_menu_added(self):
        self.client.force_login(self.test_user)
        response = self.client.post(
          reverse("menu:menu_new"),
          data=self.menu_data,
          follow=True
        )
        self.assertTemplateUsed('menu/menu_detail.html')
        self.assertContains(response, "Menu added: Summer 2020")


