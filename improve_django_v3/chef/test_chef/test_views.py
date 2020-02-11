from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class TestCreateChef_Case1(TestCase):
    ''' Verify that a visitor is able to register an
    account with an username that is not taken by
    another User.'''

    @classmethod
    def setUpTestData(cls):
        cls.user_signup_data = {
            'username': 'masterchef',
            'password1': 'secret',
            'password2': 'secret'
        }

    def test_chef_register_successful_registeration(self):
        response = self.client.post(
            reverse("chef:register"),
            self.user_signup_data,
            follow=True,
        )
        self.assertRedirects(response, reverse("menu:menu_list"))
        self.assertTemplateUsed('menu/list_all_current_menus.html')
        self.assertContains(
            response,
            "Logged in: masterchef!",
        )


class TestCreateNewChef_Case2(TestCase):
    '''Verify that a visitor cannot register an
    account with an username that happens to
    belong to a different User.'''

    '''https://docs.djangoproject.com/en/3.0/ref/models
    /instances/#django.db.models.Model.validate_unique'''

    '''Model instances are checked for uniqueness as a 
    part of the model validation process; a ValidationError
    is raised if a unique constraint is violated.'''

    '''https://github.com/django/django/blob
    /master/django/contrib/auth/models.py#L315'''

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='masterchef',
            password='password'
        )
        cls.user_signup_data = {
            'username': 'masterchef',
            'password1': 'secret',
            'password2': 'secret'
        }

    def test_chef_register_username_taken(self):
        response = self.client.post(
            reverse("chef:register"),
            self.user_signup_data,
            follow=True
        )
        self.assertTemplateUsed('chef/register_chef.html')
        self.assertContains(
            response,
            "<p>A user with that username already exists.</p>",
            html=True
        )

class TestLoginViewActiveAccount(TestCase):
    '''Verify that a User is authenticated upon
    submitting their account login credentials.'''

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='masterchef',
            password='password'
        )

        cls.login_form_data = {
            'username': 'masterchef',
            'password': 'password'
        }

    def test_login_chef_successful_login(self):
        self.client.login(
            username=self.login_form_data['username'],
            password=self.login_form_data['password']
        )
        response = self.client.post(
            reverse("chef:login"),
            self.login_form_data,
            follow=True
        )
        self.assertRedirects(response, reverse("menu:menu_list"))
        self.assertTemplateUsed('menu/list_all_current_menus.html')
        self.assertContains(response, "Welcome masterchef!")
        self.assertContains(response, "menu/new/")


class TestLoginViewNoAccount(TestCase):
    '''Verify that attempting to login into the 
    website without'''
    @classmethod
    def setUpTestData(cls):
        cls.login_form_data = {
            'username': 'masterchef',
            'password': 'password'
        }

    def test_login_chef_failed_login(self):
        response = self.client.post(
            reverse("chef:login"),
            self.login_form_data,
            follow=True
        )
        self.assertContains(response, "Login failed. Please try again")


class TestLogoutView(TestCase):
    """Verify that a user is logged out 
    of their account when they click 'Log Out'"""

    @classmethod
    def setUpTestData(cls):

        cls.menu_views = {
            'menu_list': reverse("menu:menu_list"),
            'menu_edit': reverse("menu:menu_edit", kwargs={'pk': 4}), # needs to supply primary key to function
            'menu_detail': reverse("menu:menu_detail", kwargs={'pk': 5}),
            'item_detail': reverse("menu:item_detail", kwargs={'pk': 6}), 
            'menu_new': reverse("menu:menu_new")
        }
        cls.test_user = User.objects.create_user(
            username="masterchef",
            password="secret"
        )

    def test_logout_chef_success_referer_menu_listing_page(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse("chef:logout"),
            HTTP_REFERER=self.menu_views['menu_list']
        )
        self.assertRedirects(response, reverse("menu:menu_list"))

    def test_logout_chef_success_referer_edit_menu_page(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse("chef:logout"),
            HTTP_REFERER=self.menu_views['menu_edit']
        )
        self.assertRedirects(response, reverse("menu:menu_list"))

    def test_logout_chef_success_referer_menu_detail_page(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse("chef:logout"),
            HTTP_REFERER=self.menu_views['menu_detail']
        )
        self.assertRedirects(response, reverse("menu:menu_list"))

    def test_logout_chef_success_referer_item_detail_page(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse("chef:logout"),
            HTTP_REFERER=self.menu_views['item_detail']
        )
        self.assertRedirects(response, reverse("menu:menu_list"))

    def test_logout_chef_success_referer_new_menu_page(self):
        self.client.force_login(self.test_user)
        response = self.client.get(
            reverse("chef:logout"),
            HTTP_REFERER=self.menu_views['menu_new']
        )
        self.assertRedirects(response, reverse("menu:menu_list"))