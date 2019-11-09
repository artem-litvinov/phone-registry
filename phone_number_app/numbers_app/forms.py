from django import forms


class PhoneNumberForm(forms.Form):
    code = forms.CharField(label="Code", min_length=3, max_length=3, required=True)
    number = forms.CharField(label="number", min_length=7, max_length=7, required=True)
