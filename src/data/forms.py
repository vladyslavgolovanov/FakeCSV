from django.forms import ModelForm, inlineformset_factory

from data.models import Schemas, Column


class ColumnForm(ModelForm):
    class Meta:
        model = Column
        fields = ('column_name', 'type')


ColumnFormSet = inlineformset_factory(Schemas, Column, form=ColumnForm, extra=5)

