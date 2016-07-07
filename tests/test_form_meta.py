import pytest

import django

from .test_app.models import BaseModel, RelatedModel
from .test_app.forms import BaseModelMetaForm


pytestmark = pytest.mark.django_db


@pytest.mark.skipif(django.VERSION[:2] < (1, 9),
                    reason='field_classes added in 1.9')
def test_save_meta():
    form = BaseModelMetaForm({'fk_0': 1})

    assert form.is_valid()

    form.save()

    assert BaseModel.objects.count() == 1
    assert RelatedModel.objects.count() == 1