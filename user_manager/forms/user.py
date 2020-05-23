from django import forms

class VerifiedUserForm(forms.Form):
    username = forms.CharField(max_length=20, required=True)
    password = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    captcha = forms.CharField(max_length=6, required=True)
