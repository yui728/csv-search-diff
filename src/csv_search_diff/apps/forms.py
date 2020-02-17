from django import forms
from django.forms.formsets import formset_factory, BaseFormSet
import pandas as pd
from . import utility as util


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
    def __init__(self, *args, csv1_diff_col_choices, csv2_diff_col_choices, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['csv1_diff_col'].choices = csv1_diff_col_choices
        self.fields['csv2_diff_col'].choices = csv2_diff_col_choices

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
    def __init__(self, *args, csv1_key_col_choices, csv2_key_col_choices, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['csv1_key_col'].choices = csv1_key_col_choices
        self.fields['csv2_key_col'].choices = csv2_key_col_choices

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


def create_formset(cls, max_num, min_num=1):

    return formset_factory(
        cls,
        max_num=max_num,
        min_num=min_num,
        extra=1,
        validate_max=True,
        validate_min=True
    )


def create_setting_diff_column_formset(csv1: pd.DataFrame, csv2: pd.DataFrame, data: dict = None):
    diff_column_max = util.CalcColumnCountUtility.get_max_diff_column_count(
        csv1,
        csv2
    )
    diff_column_setting_form_set = create_formset(
        DiffColumnSettingForm,
        max_num=diff_column_max
    )
    choices = {
        'csv1_diff_col_choices': column_to_choices(csv1.columns),
        'csv2_diff_col_choices': column_to_choices(csv2.columns)
    }
    # print(f'create_setting_diff_column_formset choices = {choices}')
    formset = diff_column_setting_form_set(data=data, form_kwargs=choices)
    # print(f'create_setting_diff_column_formset formset = {formset.as_p()}')
    return formset


def create_setting_key_column_formset(csv1: pd.DataFrame, csv2: pd.DataFrame, diff_key_column_count: int,data: dict = None):
    key_column_max = util.CalcColumnCountUtility.get_max_key_column_count(
        csv1,
        csv2,
        diff_key_column_count
    )
    key_column_setting_form_set = create_formset(
        KeyColumnSettingForm,
        max_num=key_column_max
    )
    choices = {
        'csv1_key_col_choices': column_to_choices(csv1.columns),
        'csv2_key_col_choices': column_to_choices(csv2.columns)
    }
    # print(f'create_setting_key_column_formset choices = {choices}')
    formset = key_column_setting_form_set(data=data, form_kwargs=choices)
    return formset


def column_to_choices(column):
    return [
                (value, text) for (value, text) in enumerate(column)
            ]

# def set_choices(formset: BaseFormSet, choices: dict) -> BaseFormSet:
#     for form in formset.forms:
#         for key, values in choices.items():
#             form.fields[key].choices = [
#                 (value, text) for (value, text) in enumerate(values)
#             ]
#
#     print(f"formset table = {formset.as_table()}")
#     return formset
