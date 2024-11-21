import random
from random import randint
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_otp.plugins.otp_static.models import StaticDevice
from .forms import UserCreationFormWithFields
def register(request):
    if request.method == 'POST':
        form = UserCreationFormWithFields(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # L'utilisateur doit vérifier son e-mail
            user.save()

            verification_code_email = randint(100000, 999999)
            cache.set(f'verification_code_email_{user.email}', verification_code_email, timeout=600)

            send_verification_email(user.email, verification_code_email)

            messages.success(request, "Un code de vérification a été envoyé à votre adresse e-mail.")
            # Correction ici : utilisez uniquement 'identifier'
            return redirect('verify', identifier=user.email)  # Passez uniquement 'identifier'
    else:
        form = UserCreationFormWithFields()
    return render(request, 'register.html', {'form': form})
def send_email(subject, to_email, body):
    """Envoi d'un e-mail via Django SendMail"""
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=None,  # Utilisera DEFAULT_FROM_EMAIL dans settings.py
            recipient_list=[to_email],
            fail_silently=False,
        )
        print(f"E-mail envoyé avec succès à {to_email}")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")


def send_verification_email(user_email, code):
    """Envoi d'un e-mail de vérification"""
    subject = "Code de vérification"
    body = f"""
        Votre code de vérification est : {code}.
        Ce code est valide pendant 10 minutes.
    """
    send_email(subject, user_email, body)


def login_view(request):
    """Connexion d'un utilisateur"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f'Bienvenue {username} ! Vous êtes connecté.')
            return redirect('home')
        else:
            messages.error(request, 'Identifiants invalides. Veuillez réessayer.')
    return render(request, 'login.html')


@login_required
def home(request):
    """Page d'accueil"""
    return render(request, 'home.html')


@login_required
def level_one(request):
    """Page pour le niveau 1"""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == "utilisateur4" and password == "01234":
            return redirect('level_one_bureau')
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect.")
    return render(request, 'level_one.html')


@login_required
def level_one_bureau(request):
    """Page pour le bureau du niveau 1"""
    return render(request, 'level_one_bureau.html')


@login_required
def level_two(request):
    """Page pour le niveau 2"""
    return render(request, 'level_two.html')


@login_required
def level_three(request):
    """Page pour le niveau 3"""
    return render(request, 'level_three.html')


def test_email(request):
    """Envoi d'un e-mail de test"""
    subject = "Test Email"
    body = "Ceci est un e-mail de test envoyé par Django."
    recipient_email = "recipient@example.com"
    try:
        send_email(subject, recipient_email, body)
        return HttpResponse("E-mail envoyé avec succès !")
    except Exception as e:
        return HttpResponse(f"Échec de l'envoi de l'e-mail : {e}")


def verify(request, method, identifier):
    if request.method == 'POST':
        code = request.POST.get('code')
        stored_code = cache.get(f'verification_code_{identifier}')

        if stored_code and str(code) == str(stored_code):
            user = get_user_model().objects.filter(email=identifier).first()
            if user:
                user.is_active = True
                user.save()
                cache.delete(f'verification_code_{identifier}')
                messages.success(request, "Votre compte a été vérifié avec succès!")
                return redirect('home')  # Redirige vers la page d'accueil
            else:
                messages.error(request, "Utilisateur non trouvé.")
        else:
            messages.error(request, "Code incorrect ou expiré. Veuillez réessayer.")

    return render(request, 'verify.html', {'method': method, 'identifier': identifier})