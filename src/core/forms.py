from django import forms


class DateForm(forms.Form):
    """Форма для получения интервала."""

    start_date = forms.DateField()
    end_date = forms.DateField()
