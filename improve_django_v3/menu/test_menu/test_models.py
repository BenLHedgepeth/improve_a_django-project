from django.test import SimpleTestCase, TestCase
from django.contrib.auth.models import User
from django.utils import timezone

from ..models import Item, Ingredient, Menu


class TestModelStrMethod(SimpleTestCase):
    ''' Verify that calling str() on a model instance
    returns a string representation of the model.'''

    def setUp(self):
        self.test_item = Item(name="Crepe")
        self.test_ingredient = Ingredient(name="Flour")
        self.test_menu = Menu(season="Spring")

    def test_item_instance_str(self):
        self.assertEqual(str(self.test_item), 'Crepe')

    def test_ingredient_instance_str(self):
        self.assertEqual(str(self.test_ingredient), 'Flour')

    def test_menu_instance_str(self):
        self.assertEqual(str(self.test_menu), 'Spring')


class TestModelURL(TestCase):
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
        cls.item.ingredients.add(eggs, flour, milk, butter, vanilla_extract, sugar) # watch for potential error when running test
        cls.menu = Menu.objects.create(
            season="Fall"
        )
        cls.menu.items.add(cls.item)

    def test_menu_absolute_url(self):
        menu = Menu.objects.get(season="Fall")
        self.assertEqual(menu.get_absolute_url(), '/menu/1/')

    def test_item_absolute_url(self):
        item = Item.objects.get(name="Crepe")
        self.assertEqual(item.get_absolute_url(), '/menu/item/1/')
