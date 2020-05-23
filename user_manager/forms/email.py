from django import forms


class VerifiedEmail(forms.Form):
    email = forms.EmailField(required=True)
