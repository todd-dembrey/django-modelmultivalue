from django import forms

from .models import BaseModel, RelatedModel
from modelmultivalue import ModelMultiValueField


class BaseModelForm(forms.ModelForm):
    class Meta:
        model = BaseModel
        fields = '__all__'

    fk = ModelMultiValueField(model=RelatedModel)
