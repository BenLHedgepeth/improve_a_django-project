import re

from django.core.exceptions import ValidationError

def validate_season(value):
    if all((season not in value 
        for season in ['Summer', 'Spring', 'Fall', 'Winter'])):
        raise ValidationError(
            message='''Specify whether the menu falls within the Summer, Fall, Winter, or Spring.''',
            code='invalid_season'
        )

def validate_meal(value):
	if value not in ['Breakfast', 'Lunch', 'Dinner']:
		raise ValidationError("Select Breakfast, Lunch, or Dinner for the meal.")