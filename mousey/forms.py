from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class UserCreationFormWithFields(UserCreationForm):
    phone_number = forms.CharField(
        required=True,
        label="Numéro de téléphone",
        widget=forms.TextInput(attrs={'placeholder': 'Ex: +33012345678'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'password1', 'password2']

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("Ce numéro de téléphone est déjà utilisé.")
        return phone_number
