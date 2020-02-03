from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Menu, Item
from django.utils.translation import ugettext_lazy as _

from .form_utils import validate_season

class MenuForm(forms.ModelForm):
    MENU_YEARS = [2019, 2020, 2021]

    season = forms.CharField(
        min_length=4, 
        validators=[validate_season]
    )
    items = forms.ModelMultipleChoiceField(
        queryset=Item.objects.all(),
        to_field_name='name'
    )
    expiration_date = forms.DateTimeField(
        required=False,
        widget=SelectDateWidget(
            years=MENU_YEARS,
            empty_label=("Choose Year", "Choose Month", "Choose Day")
        )
    )

    def clean(self):
        cleaned_data = super().clean()
        created_date = cleaned_data['created_date'] = timezone.now()
        expiration_date = cleaned_data['expiration_date']
        if created_date > expiration_date:
            raise ValidationError("Boo!", code="invalid_expiration")
        else:
            return cleaned_data

    class Meta:
        model = Menu
        fields = ['season', 'items', 'expiration_date']

