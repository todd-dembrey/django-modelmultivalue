from django import forms

from .models import BaseModel, RelatedModel, MultiFieldModel, MultiFieldRelatedModel
from modelmultivalue import ModelMultiValueField


class BaseModelForm(forms.ModelForm):
    class Meta:
        model = BaseModel
        fields = '__all__'

    fk = ModelMultiValueField(model=RelatedModel)


class BaseModelMetaForm(forms.ModelForm):
    class Meta:
        model = BaseModel
        fields = '__all__'
        field_classes = {
            'fk': ModelMultiValueField,
        }


class MultiFieldModelForm(forms.ModelForm):
    class Meta:
        model = MultiFieldModel
        fields = '__all__'

    fk = ModelMultiValueField(model=MultiFieldRelatedModel)
