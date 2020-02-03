from __future__ import unicode_literals

from django.db import migrations
from django.db.models import Min

def remove_duplicates(apps, schema_editor):
    Menu = apps.get_model('menu', 'Menu')
    seasonal_menus = set(list(Menu.objects.values_list('season', flat=True)))
    for season in seasonal_menus:
        seasonal_menus = Menu.objects.filter(season=season)
        if seasonal_menus.count() > 1:
            # calculate the smallest primary key for all menu instances that share the same season
            instance = seasonal_menus.aggregate(menu_id=Min('id'))
            seasonal_menus.exclude(id=instance["menu_id"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20160406_1554'),
    ]

    operations = [
        migrations.RunPython(remove_duplicates, migrations.RunPython.noop)
    ]
