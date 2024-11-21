from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User, AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=False)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label="Adresse e-mail",
        widget=forms.EmailInput(attrs={'placeholder': 'Adresse e-mail'})
    )


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'id': 'id_username', 'placeholder': "Nom d'utilisateur"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'id': 'id_password', 'placeholder': 'Mot de passe'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
