from django import forms
from .models import Lens, LensComponent

class CreatefieldsForm(forms.Form):

    lensfields = [f.name for f in Lens._meta.get_fields()]
    compfields = [f.name for f in LensComponent._meta.get_fields()]
    #print(compfields, lensfields)
    fields = lensfields[2:] + compfields[2:]
    options = []
    for i in range(len(fields)):
        options.append((i,fields[i]))

    fieldform = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=options,
    )