from django import forms
from django.forms.formsets import formset_factory


class CsvInputForm(forms.Form):
    csv1 = forms.fields.FileField(
        label='CSV1',
        required=True,
        widget=forms.widgets.FileInput
    )

    csv1_no_header = forms.fields.BooleanField(
        label='ヘッダーなし',
        required=False,
        widget=forms.widgets.CheckboxInput
    )

    csv2 = forms.fields.FileField(
        label='CSV2',
        required=True,
        widget=forms.widgets.FileInput
    )

    csv2_no_header = forms.fields.BooleanField(
        label='ヘッダーなし',
        required=False,
        widget=forms.widgets.CheckboxInput
    )


class DiffColumnSettingForm(forms.Form):
    csv1_diff_col = forms.fields.ChoiceField(
        label='',
        required=True,
        widget=forms.widgets.Select
    )

    csv2_diff_col = forms.fields.ChoiceField(
        label='',
        required=True,
        widget=forms.widgets.Select
    )


DiffColumnSettingFormSet = formset_factory(DiffColumnSettingForm)

# class KeyColumnSettingForm(forms.Form):
#
#
# class ConfirmForm(forms.Form):
#
#
# class ResultForm(forms.Form):

