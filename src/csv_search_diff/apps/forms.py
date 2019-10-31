from django import forms


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
    csv1_diff_col = forms.fields.MultipleChoiceField(
        label='',
        required=True,
        widget=forms.widgets.Select
    )

    csv2_diff_col = forms.fields.MultipleChoiceField(
        label='',
        required=True,
        widget=forms.widgets.Select
    )

    def is_valid(self):
        result = super().is_valid()
        if result:
            cleaned_data = self.cleaned_data
            if not len(cleaned_data['csv1_diff_col']) == len(cleaned_data['csv2_diff_col']):
                result = False
                self.add_error(None, 'CSV1とCSV2の比較項目の数が違います。')
        return result



# class KeyColumnSettingForm(forms.Form):
#
#
# class ConfirmForm(forms.Form):
#
#
# class ResultForm(forms.Form):

