import pytest

import django


django_18_field_class_skip = pytest.mark.skipif(django.VERSION[:2] < (1, 9),
                                                reason='field_classes added in 1.9')
