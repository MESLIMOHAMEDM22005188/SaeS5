import os
from random import random

from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.cache import cache

from mousey.forms import CustomUserCreationForm


def verify_email(request, email):
    if request.method == 'POST':
        code = request.POST.get('code')
        stored_code = cache.get(f'verification_code_{email}')

        if str(code) == str(stored_code):
            user = User.objects.get(email=email)
            user.is_active = True  # Active l'utilisateur
            user.save()
            cache.delete(f'verification_code_{email}')  # Supprime le code du cache
            messages.success(request, "Votre compte a été vérifié avec succès !")
            return redirect('login')
        else:
            messages.error(request, "Code de vérification incorrect ou expiré.")

    return render(request, 'verify_email.html', {'email': email})


def send_verification_email(user_email, code):
    subject = "Code de vérification"
    body = f"""
        <h1>Code de vérification</h1>
        <p>Votre code est : <strong>{code}</strong></p>
        <p>Ce code est valide pendant 10 minutes.</p>
    """
    return send_email(subject, user_email, body)


def send_email(subject, to_email, body):
    try:
        message = Mail(
            from_email="test@example.com",  # Adresse d'envoi
            to_emails=to_email,
            subject=subject,
            html_content=body
        )
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(f"Email envoyé avec le statut: {response.status_code}")
        return response
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail: {e}")  # Affichez les détails de l'erreur
        return None


# Vue pour tester l'envoi d'un e-mail
def test_email(request):
    subject = "Test Email avec Mailtrap"
    body = "Ceci est un test d'e-mail avec Mailtrap et Django."
    recipient_email = "recipient@example.com"  # Adresse de réception

    email_status = send_email(subject, recipient_email, body)
    if email_status:
        return HttpResponse("E-mail envoyé avec succès !")
    else:
        import random  # Assurez-vous que cette ligne est présente
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f'Bienvenue {username} ! Vous êtes connecté.')
                return redirect('home')
            else:
                messages.error(request, 'Identifiants invalides. Veuillez réessayer.')
        else:
            messages.error(request, 'Identifiants invalides. Veuillez réessayer.')
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})


# Vue pour la page d'accueil
@login_required
def home(request):
    return render(request, 'home.html')


# Vue pour le niveau 1
@login_required
def level_one(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "utilisateur4" and password == "01234":
            return redirect('level_one_bureau')
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect.")

    return render(request, 'level_one.html')


# Vue pour le bureau du niveau 1
@login_required
def level_one_bureau(request):
    return render(request, 'level_one_bureau.html')


# Vue pour le niveau 2
@login_required
def level_two(request):
    return render(request, 'level_two.html')


# Vue pour le niveau 3
@login_required
def level_three(request):
    return render(request, 'level_three.html')
