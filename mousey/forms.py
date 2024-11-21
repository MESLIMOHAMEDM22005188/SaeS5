from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreationFormWithFields(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={'placeholder': 'Adresse e-mail'}),
    )
    phone_number = forms.CharField(
        required=True,
        label="Numéro de téléphone",
        widget=forms.TextInput(attrs={'placeholder': 'Numéro de téléphone'}),
    )

    class Meta:
        model = User  # Modèle par défaut de Django
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Un compte avec cet e-mail existe déjà.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(username=phone_number).exists():
            raise forms.ValidationError("Ce numéro de téléphone est déjà utilisé.")
        return phone_number
