from django.conf.urls import url
from . import views

app_name = "chef"

urlpatterns = [
	url(r'^login/$', views.login_chef, name="login"),
	url(r'^register/$', views.register_chef, name="register")
]