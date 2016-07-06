from django import forms
from django.forms import ValidationError

from .widgets import ModelMultiValueWidget


class ModelMultiValueField(forms.MultiValueField):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.model_form = forms.models.modelform_factory(self.model, fields='__all__')
        kwargs.update({'required': False,
                       'require_all_fields': False
                       })
        fields = [
            field for field in self.model_form.base_fields.values()
        ]
        self.widget = ModelMultiValueWidget(widgets=[field.widget for field in fields],
                                            field_names=self.model_form.base_fields.keys(),
                                            labels=[field.label for field in fields],
                                            model=self.model
                                            )
        super(ModelMultiValueField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list:
            attrs = dict((field, value) for field, value in zip(self.model_form.base_fields.keys(), data_list))
            return self.model.objects.create(**attrs)
        else:
            raise ValidationError('Could not create model', code='poor_data')
