import pytest

from .test_app.models import BaseModel, RelatedModel
from .test_app.forms import ChoiceAndMultiForm


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
