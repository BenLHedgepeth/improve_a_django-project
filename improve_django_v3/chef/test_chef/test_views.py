from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class TestCreateNewChef(TestCase):

    @classmethod
    def setUpTestData(cls):

        cls.user_signup_data = {
            'username': 'masterchef',
            'password1': 'secret',
            'password2': 'secret'
        }


    def test_new_chef_sign_up_success(self):

        response = self.client.post(
            reverse("chef:register"), 
            self.user_signup_data,
            follow=True
        )
        self.assertRedirects(response, reverse("menu:menu_list"))
        self.assertTemplatedUsed('menu/list_all_current_menus.html')
        self.assertContains(
            response,
            "<p>Logged in: masterchef!</p>",
            html=True
        )
