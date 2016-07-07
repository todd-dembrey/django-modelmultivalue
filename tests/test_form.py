import pytest

from django.forms.models import modelform_factory
from django.core.exceptions import ImproperlyConfigured

from modelmultivalue import ModelMultiValueField

from .test_app.models import BaseModel, RelatedModel, DefaultBaseModel, DefaultModel, NullBaseModel, NullModel, MultiFieldModel, MultiFieldRelatedModel
from .test_app.forms import BaseModelForm, MultiFieldModelForm


pytestmark = pytest.mark.django_db


def test_save():
    form = BaseModelForm({'fk_0': 1})

    assert form.is_valid()

    form.save()

    assert BaseModel.objects.count() == 1
    assert RelatedModel.objects.count() == 1


@pytest.mark.parametrize(
    'form, data', (
            (BaseModelForm, {'fk_0': 'xyz*|\\'}),
            (BaseModelForm, {'fk_0': ''}),
            (MultiFieldModelForm, {'fk_0': '', 'fk_1': ''}),
    )
)
def test_form_is_invalid(form, data):
    assert not form(data).is_valid()


@pytest.mark.parametrize(
    'parent_model, related_model', (
            (MultiFieldModel, MultiFieldRelatedModel),
            (DefaultBaseModel, DefaultModel),
            (NullBaseModel, NullModel),
    )
)
def test_non_blank_raise_error(parent_model, related_model):
    with pytest.raises(ImproperlyConfigured):
        modelform_factory(parent_model,
                          fields='__all__',
                          widgets={'fk': ModelMultiValueField(model=related_model,
                                                              fields=['test_field_0'])})


@pytest.mark.parametrize(
    'parent_model, related_model, fields', (
            (MultiFieldModel, MultiFieldRelatedModel, ['test_field_0', 'test_field_1']),
            (DefaultBaseModel, DefaultModel, ['test_field_1']),
            (NullBaseModel, NullModel, ['test_field_1']),
    )
)
def test_doesnt_raise_error(parent_model, related_model, fields):

    def fk_callback(field, **kwargs):
        if field.name == 'fk':
            return ModelMultiValueField(model=related_model, fields=fields)
        else:
            return field.formfield(**kwargs)

    Form = modelform_factory(parent_model,
                             fields='__all__',
                             formfield_callback=fk_callback)

    form = Form({'fk_0': 0, 'fk_1': 1})

    assert form.is_valid()

    instance = form.save()

    assert parent_model.objects.count() == 1
    assert related_model.objects.count() == 1


def test_no_model_in_init():
    with pytest.raises(ImproperlyConfigured):
        ModelMultiValueField()
