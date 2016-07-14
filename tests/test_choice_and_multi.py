import pytest

from .conftest import django_18_field_class_skip

from .test_app.models import BaseModel, RelatedModel, MultiFieldModel, MultiFieldRelatedModel
from .test_app.forms import ChoiceAndMultiForm, ChoiceAndMultipleFieldForm


pytestmark = pytest.mark.django_db

fields = 'test_form, parent_model, related_model, fields'
test_data = (
            (ChoiceAndMultiForm, BaseModel, RelatedModel, {'test_field': 1}),
            (ChoiceAndMultipleFieldForm, MultiFieldModel, MultiFieldRelatedModel, {'test_field_0': 1, 'test_field_1': 1}),
    )
test_input = (fields, test_data)


@django_18_field_class_skip
@pytest.mark.parametrize(*test_input)
def test_save_multi(test_form, parent_model, related_model, fields):
    form_dict = {'fk_{}'.format(i+1): field for i, field in enumerate(fields.values())}
    form = test_form(form_dict)

    assert form.is_valid()

    form.save()

    assert parent_model.objects.count() == 1
    assert related_model.objects.count() == 1


@django_18_field_class_skip
@pytest.mark.parametrize(*test_input)
def test_save_choice(test_form, parent_model, related_model, fields):
    related = related_model.objects.create(**fields)

    assert related_model.objects.count() == 1

    form = test_form({'fk_0': related.pk})

    assert form.is_valid()

    form.save()

    assert parent_model.objects.count() == 1
    assert related_model.objects.count() == 1
