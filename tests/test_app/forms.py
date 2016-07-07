from django import forms

from .models import BaseModel, RelatedModel, MultiFieldModel, MultiFieldRelatedModel
from modelmultivalue import ModelMultiValueField


class BaseModelForm(forms.ModelForm):
    class Meta:
        model = BaseModel
        fields = '__all__'

    fk = ModelMultiValueField(model=RelatedModel)


class MultiFieldModelForm(forms.ModelForm):
    class Meta:
        model = MultiFieldModel
        fields = '__all__'

    fk = ModelMultiValueField(model=MultiFieldRelatedModel)
