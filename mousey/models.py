from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User, AbstractUser, Permission, Group
from django.db import models

from mickey.settings import BASE_DIR


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=False)

    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Nom personnalisé pour éviter le conflit
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_set_permissions",  # Nom personnalisé pour éviter le conflit
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


STATIC_URL = '/static/'

# Dossier où collecter les fichiers statiques (production uniquement)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Répertoires supplémentaires pour rechercher les fichiers statiques
STATICFILES_DIRS = [
    BASE_DIR / "static",  # Dossier local pour les fichiers statiques
]


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
