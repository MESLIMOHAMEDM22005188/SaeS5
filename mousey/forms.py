from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreationFormWithFields(UserCreationForm):
    phone_number = forms.CharField(
        required=True,
        label="Numéro de téléphone",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: +33612345678'}),
    )

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password1', 'password2']
