====================
ModelMultiValueField
====================

ModelMultiValueField provides the ability to create sub-forms for foreign models without having to worry about writing
the multivaluefield subclasses.

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

        ForeignKeyField = ModelMultiValueField()
