import random
from random import randint
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_otp.plugins.otp_static.models import StaticDevice
from .forms import UserCreationForm


def register(request):
    """Inscription d'un nouvel utilisateur"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Génération des codes de vérification
            verification_code_email = randint(100000, 999999)
            verification_code_phone = randint(100000, 999999)

            # Stockage des codes dans le cache
            cache.set(f'verification_code_email_{user.email}', verification_code_email, timeout=600)
            cache.set(f'verification_code_phone_{user.phone_number}', verification_code_phone, timeout=600)

            # Envoi des codes
            send_verification_email(user.email, verification_code_email)
            send_sms(user.phone_number, verification_code_phone)

            messages.success(request, "Des codes de vérification ont été envoyés.")
            return redirect('verify', method='email', identifier=user.email)
    else:
        form = UserCreationForm()
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
    """Vérification du compte utilisateur"""
    if request.method == 'POST':
        code = request.POST.get('code')
        stored_code = cache.get(f'verification_code_{identifier}')
        if stored_code and str(code) == str(stored_code):
            user = User.objects.filter(email=identifier).first() if method == "email" else User.objects.filter(
                phone_number=identifier).first()
            if user:
                user.is_active = True
                user.save()
                cache.delete(f'verification_code_{identifier}')
                messages.success(request, "Votre compte a été vérifié avec succès !")
                return redirect('home')
            messages.error(request, "Utilisateur non trouvé.")
        else:
            messages.error(request, "Code incorrect ou expiré. Veuillez réessayer.")
    return render(request, 'verify.html', {'method': method, 'identifier': identifier})


def send_sms(phone_number, code):
    """Simule l'envoi de SMS"""
    print(f"Code {code} envoyé au numéro {phone_number}")


@login_required
def enable_2fa_phone(request):
    """Activer l'authentification à deux facteurs par téléphone"""
    if request.method == "POST":
        code = random.randint(100000, 999999)
        device = StaticDevice.objects.create(user=request.user, name="Téléphone")
        device.token_set.create(token=code)
        send_sms(request.user.phone_number, code)
        messages.info(request, "Un code de vérification a été envoyé sur votre téléphone.")
        return redirect('verify_2fa_phone')
    return render(request, 'enable_2fa_phone.html')


@login_required
def verify_2fa_phone(request):
    """Vérification de l'authentification à deux facteurs"""
    if request.method == 'POST':
        code = request.POST.get('code')
        device = StaticDevice.objects.filter(user=request.user).first()
        if device and device.token_set.filter(token=code).exists():
            messages.success(request, "L'A2F est activée avec succès.")
            return redirect('home')
        messages.error(request, "Code incorrect. Veuillez réessayer.")
    return render(request, 'verify_2fa_phone.html')
