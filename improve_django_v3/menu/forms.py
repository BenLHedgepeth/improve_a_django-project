import re

from django import forms
from django.forms.extras.widgets import SelectDateWidget
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Menu, Item

from .form_utils import validate_season


class MenuForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = "form_text_widget"
            field.widget.attrs['placeholder'] = field.label

    MENU_YEARS = [2019, 2020, 2021]

    season = forms.CharField(
        min_length=4,
        validators=[validate_season],
        label="Season",
        error_messages={
            'required': "Provide a seasonal menu title"
        }
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
        menu_season = self.cleaned_data['season']
        created_date = cleaned_data['created_date'] = timezone.now()
        expiration_date = cleaned_data.get('expiration_date', None)
        ''' Accessing 'expiration_date' with bracket notation results in
        a KeyError. This was fixed by implementing `.get()` and setting 
        a default value to None upon no there was no key named 
        'expiration_date'.'''

        '''A result of the aforementioned only happens if a user partially
        selects the values required to create a datetime objects. IE. a user
        picks a year and a month, but does not select a day.'''


        if expiration_date:
            if created_date > expiration_date:
                raise ValidationError(
                    "Invalid expiration date",
                    code="invalid_expiration_date"
                )
            else:
                _menu_year = re.search(r"\d{4}", menu_season)
                if _menu_year:
                    menu_year = _menu_year.group()
                    if int(menu_year) > expiration_date.year:
                        raise ValidationError(
                            "The menu title postdates its expiration date",
                            code="post_date_error"
                        )
        else:
            return cleaned_data

    class Meta:
        model = Menu
        fields = ['season', 'items', 'expiration_date']
