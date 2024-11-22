from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserCreationFormWithFields(UserCreationForm):
    email = forms.EmailField(
        required=True,  # Le champ email est requis
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={'placeholder': 'Adresse e-mail'}),
    )

    class Meta:
        model = User  # Utilise le modèle User par défaut de Django
        fields = ['username', 'email', 'password1', 'password2']

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

