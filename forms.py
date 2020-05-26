from django import forms


class UserForm(forms.Form):
    Ticker1 = forms.CharField(max_length=100)
    start_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1980, 2021)))
    end_date = forms.DateField(
        widget=forms.SelectDateWidget(years=range(1980, 2021)))
