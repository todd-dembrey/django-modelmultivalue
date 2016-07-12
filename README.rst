====================
ModelMultiValueField
====================

ModelMultiValueField provides the ability to create sub-forms for foreign models without having to worry about writing
the ModelMultiValueField subclasses.

Quick start
-----------

1. Add "modelmultivalue" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'modelmultivalue',
    ]

2. Add the modelmultivaluefield to a model form::

    from django import forms
    from modelmultivalue import ModelMultiValueField

    class ExampleModelForm(forms.ModelForm):
        class Meta:
            model = Example
            fields = '__all__'

        ForeignKeyField = ModelMultiValueField(model=ForeignKey

or for Django>=1.9::

    from django import forms
    from modelmultivalue import ModelMultiValueField

    class ExampleModelForm(forms.ModelForm):
        class Meta:
            model = Example
            fields = '__all__'
            field_class_field={
                'ForeignKeyField': ModelMultiValueField
            }
