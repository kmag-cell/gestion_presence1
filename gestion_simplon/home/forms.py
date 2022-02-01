from django import forms
from . models import Apprenant

class ApprenantForm(forms.Form):
    class Meta:
        model = Apprenant
        fields = (
            'username',
            'password',

        )