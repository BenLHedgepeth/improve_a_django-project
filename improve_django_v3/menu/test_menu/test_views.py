from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse

# class TestMenuListView(TestCase):

#     def test_menu_list_view(self):
#         response = self.client.get(reverse("menu:menu_list"))
#         self.assertTemplateUsed('menu/list_all_current_menus.html')



# # class TestNewMenuView(TestCase):
# # 	'''Verify that a chef is authenticated'''

# # 	@classmethod
# # 	def setUpTestData(cls):

# # 		factory = RequestFactory()
# # 		users = {
# # 			'user': User.objects.create_user('test_chef', password="secret"),
# # 			'anonymous_user': AnonymousUser()
# # 		}


# # 	def test_chef_logged_in(self):
# # 		request = self.factory.get(reverse("menu:menu_new"))