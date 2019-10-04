from django import forms

class CsvInputForm(forms.Form):
    csv1 = forms.fields.FileField(
        label='CSV1',

    )