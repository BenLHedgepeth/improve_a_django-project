import re

from django.core.exceptions import ValidationError

def validate_username(value):
	match = re.search(r"\W+", value)
	if match:
		raise ValidationError("Username must only contain characters: [A-Z; a-z, 0-9, _]")