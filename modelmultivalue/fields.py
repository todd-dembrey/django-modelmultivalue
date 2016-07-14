from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.forms import ValidationError, ALL_FIELDS

from .widgets import ModelMultiValueWidget, SelectModelMultiValueWidget


class BaseModelMulti(forms.MultiValueField):
    widget_class = None

    def __init__(self, model=None, fields=ALL_FIELDS, *args, **kwargs):
        if model is None:
            try:
                self.model = kwargs.pop('queryset', None).model
            except AttributeError:
                raise ImproperlyConfigured('Field must be created with a model', 'no_model_provided')
        else:
            self.model = model

        if not fields == ALL_FIELDS:
            # Check if we've missed any required fields
            required_fields = set(name for name, field in forms.models.fields_for_model(self.model).items()
                                  if field.required)
            missing_fields = required_fields - set(fields)
            if missing_fields:
                raise ImproperlyConfigured(
                    'The following required fields were missing: {}'.format(', '.join(missing_fields)),
                    'missing_required_fields')

        model_form = forms.models.modelform_factory(self.model,
                                                    fields=fields)

        self.form_fields = [
            field for field in model_form.base_fields.values()
            ]

        self.field_names = list(model_form.base_fields.keys())

        self.widget = self.widget_class(**self.widget_kwargs())
        # Remove kwargs that aren't needed TODO: Confirm not needed
        kwargs.pop('limit_choices_to', None)
        kwargs.pop('to_field_name', None)

        # This allows the sub widgets to be blank
        kwargs.update({'required': False,
                       'require_all_fields': False
                       })

        super(BaseModelMulti, self).__init__(self.form_fields, *args, **kwargs)

    def widget_kwargs(self):
        return {'widgets': [field.widget for field in self.form_fields],
                'field_names': self.field_names,
                'labels': [field.label for field in self.form_fields],
                'model': self.model
                }

    def compress(self, data_list):
        if data_list:
            attrs = dict((field, value) for field, value in zip(self.field_names, data_list))
            return self.model.objects.create(**attrs)
        else:
            raise ValidationError('Could not create model', code='poor_data')


class ModelMultiValueField(BaseModelMulti):
    """A field class which provides a sub-form for a model.
    """
    widget_class = ModelMultiValueWidget


class ModelChoiceAndMultiField(BaseModelMulti):
    """A field class which provides a select field and a sub-form for a model.

    The select field takes priority over the sub-form.

    This doesn't work with django < 1.9
    """
    widget_class = SelectModelMultiValueWidget

    def __init__(self, *args, **kwargs):
        kwargs.update({'required': False})
        self.select = forms.ModelChoiceField(*args, **kwargs)
        super(ModelChoiceAndMultiField, self).__init__(*args, **kwargs)
        self.fields.insert(0, self.select)

    def widget_kwargs(self):
        kwargs = super(ModelChoiceAndMultiField, self).widget_kwargs()
        kwargs.update({'select': self.select})
        return kwargs

    def compress(self, data_list):
        try:
            object_id = data_list.pop(0)
            return self.model.objects.get(id=object_id)
        except (IndexError, self.model.DoesNotExist):
            return super(ModelChoiceAndMultiField, self).compress(data_list)

    def clean(self, value):
        out = self.fields[0].clean(value[0])
        if not out:
            return super(ModelChoiceAndMultiField, self).clean(value)
        return out
