import pytest

from .conftest import django_18_field_class_skip

from .test_app.models import BaseModel, RelatedModel
from .test_app.forms import BaseModelMetaForm


pytestmark = pytest.mark.django_db


@django_18_field_class_skip
def test_save_meta():
    form = BaseModelMetaForm({'fk_0': 1})

    assert form.is_valid()

    form.save()

    assert BaseModel.objects.count() == 1
    assert RelatedModel.objects.count() == 1