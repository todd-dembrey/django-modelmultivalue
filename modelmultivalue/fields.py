from django import forms
from django.core.exceptions import ImproperlyConfigured
from django.forms import ValidationError, ALL_FIELDS

from .widgets import ModelMultiValueWidget


class ModelMultiValueField(forms.MultiValueField):
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

        self.model_form = forms.models.modelform_factory(self.model,
                                                         fields=fields)

        form_fields = [
            field for field in self.model_form.base_fields.values()
        ]

        self.widget = ModelMultiValueWidget(widgets=[field.widget for field in form_fields],
                                            field_names=self.model_form.base_fields.keys(),
                                            labels=[field.label for field in form_fields],
                                            model=self.model
                                            )
        # Remove kwargs that aren't needed TODO: Confirm not needed
        kwargs.pop('limit_choices_to', None)
        kwargs.pop('to_field_name', None)

        # This allows the sub widgets to be blank
        kwargs.update({'required': False,
                       'require_all_fields': False
                       })

        super(ModelMultiValueField, self).__init__(form_fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            attrs = dict((field, value) for field, value in zip(self.model_form.base_fields.keys(), data_list))
            return self.model.objects.create(**attrs)
        else:
            raise ValidationError('Could not create model', code='poor_data')
