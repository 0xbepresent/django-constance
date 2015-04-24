from django import forms
from django.core.exceptions import ValidationError
from django.forms.widgets import MultipleHiddenInput
from django.utils.encoding import smart_text


class CommaSeparatedList(forms.CharField):
    """Custom Form para poder manejar una lista de valores separada por comas"""

    widget = forms.Textarea
    default_error_messages = {
        'invalid_list': ('Introduzca una serie de valores separados por comas.'),
    }

    def clean(self, value):
        lresult = []
        try:
            # Normalizando valores que llegan de Django-Admin
            result = value.replace("[", "")
            result = result.replace("]", "")
            result = result.replace("'", "")
            result = result.replace("\"", "")
            result = result.split(',')

            # Poder manejar una lista de valores enumericos y cadenas.
            for val in result:
                try:
                    lresult.append(int(val))
                except:
                    lresult.append(str(val.strip()))
        except:
            raise ValidationError(self.error_messages['invalid_list'], code='invalid_list')
        value = lresult
        return super(CommaSeparatedList, self).clean(value)

    def to_python(self, value):
        if not value:
            return []
        elif not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['invalid_list'], code='invalid_list')
        return value

    def validate(self, value):
        """
        Validates that the input is a list or tuple.
        """
        if self.required and not value:
            raise ValidationError(self.error_messages['required'], code='required')
        if not isinstance(value, (list, tuple)):
            raise ValidationError(self.error_messages['invalid_list'], code='invalid_list')
        return super(CommaSeparatedList, self).validate(value)

    def has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        return data_set != initial_set
