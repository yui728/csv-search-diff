from django import forms
from django.forms.formsets import formset_factory, BaseFormSet


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


class KeyColumnSettingForm(forms.Form):
    csv1_key_col = forms.fields.ChoiceField(
        label='',
        required=True,
        widget=forms.widgets.Select
    )

    csv2_key_col = forms.fields.ChoiceField(
        label='',
        required=True,
        widget=forms.widgets.Select
    )

# class ConfirmForm(forms.Form):
#
#
# class ResultForm(forms.Form):


def create_formset(cls, max_num):

    return formset_factory(
        cls,
        max_num=max_num,
        extra=1,
        validate_max=True
    )
