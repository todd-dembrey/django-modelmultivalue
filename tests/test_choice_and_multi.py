import pytest

from .test_app.models import BaseModel, RelatedModel, MultiFieldModel, MultiFieldRelatedModel
from .test_app.forms import ChoiceAndMultiForm, ChoiceAndMultipleFieldForm


pytestmark = pytest.mark.django_db


def test_save_multi():
    form = ChoiceAndMultiForm({'fk_1': 1})

    assert form.is_valid()

    form.save()

    assert BaseModel.objects.count() == 1
    assert RelatedModel.objects.count() == 1


def test_save_choice():
    related = RelatedModel.objects.create(test_field=1)

    assert RelatedModel.objects.count() == 1

    form = ChoiceAndMultiForm({'fk_0': related.pk})

    assert form.is_valid()

    form.save()

    assert BaseModel.objects.count() == 1
    assert RelatedModel.objects.count() == 1


def test_save_multi_field():
    form = ChoiceAndMultipleFieldForm({'fk_1': 1,
                                       'fk_2': 2})

    assert form.is_valid()

    form.save()

    assert MultiFieldModel.objects.count() == 1
    assert MultiFieldRelatedModel.objects.count() == 1


def test_save_choice_multi_field():
    related = MultiFieldRelatedModel.objects.create(test_field_0=1,
                                                    test_field_1=1)

    assert MultiFieldRelatedModel.objects.count() == 1

    form = ChoiceAndMultipleFieldForm({'fk_0': related.pk})

    assert form.is_valid()

    form.save()

    assert MultiFieldModel.objects.count() == 1
    assert MultiFieldRelatedModel.objects.count() == 1
