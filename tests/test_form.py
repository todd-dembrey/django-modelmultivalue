import pytest

from .test_app.models import BaseModel, RelatedModel
from .test_app.forms import BaseModelForm


pytestmark = pytest.mark.django_db


def test_save():
    form = BaseModelForm({'fk_0': 1})

    assert form.is_valid()

    form.save()

    assert BaseModel.objects.count() == 1
    assert RelatedModel.objects.count() == 1


@pytest.mark.parametrize(
    'data',
    (
        {'fk_0': 'xyz*|\\'},
        {'fk_0': ''},
    )
)
def test_form_is_invalid(data):
    assert not BaseModelForm(data).is_valid()
