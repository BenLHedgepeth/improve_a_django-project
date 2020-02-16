from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


class Menu(models.Model):
    season = models.CharField(max_length=20, unique=True)
    items = models.ManyToManyField('Item', related_name='items')
    created_date = models.DateTimeField(default=timezone.now)
    expiration_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.season

    def get_absolute_url(self):
        return reverse("menu:menu_detail", kwargs={'pk': self.id})

    class Meta:
        ordering = ['-expiration_date']


class Item(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    chef = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    created_date = models.DateTimeField(default=timezone.now)
    standard = models.BooleanField(default=False)
    ingredients = models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("menu:item_detail", kwargs={'pk': self.pk})

class Ingredient(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name
