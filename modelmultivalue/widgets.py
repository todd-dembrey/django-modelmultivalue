from django import forms


class ModelMultiValueWidget(forms.MultiWidget):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model')
        self.labels = kwargs.pop('labels', [None])
        self.field_names = kwargs.pop('field_names', [None])
        super(ModelMultiValueWidget, self).__init__(*args, **kwargs)

    def decompress(self, value):
        if value:
            obj = self.model.objects.get(pk=value)
            return [getattr(obj, label, None) for label in self.field_names]
        return [None]*len(self.labels)

    def format_output(self, rendered_widgets):
        output = ''.join(['<p><label for="id_{model_name}_{i}">{label}:</label>{widget}</p>'.format(i=i,
                                                                                                    model_name=self.model._meta.verbose_name,
                                                                                                    label=label if label else '',
                                                                                                    widget=widget)
                          for i, (widget, label) in enumerate(zip(rendered_widgets, self.labels))])
        return output
