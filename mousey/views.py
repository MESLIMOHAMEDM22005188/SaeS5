import os
import random
from random import randint
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django_otp.plugins.otp_static.models import StaticDevice
from sendgrid.helpers.mail import email

from .forms import CustomUserCreationForm

@login_required
def verify(request, method, identifier):
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


def login_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request, data=request.POST)
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
        form = CustomUserCreationForm()
    return render(request, 'login.html', {'form': form})

def register(request):
    """Inscription d'un nouvel utilisateur"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            verification_code_email = randint(100000, 999999)
            verification_code_phone = randint(100000, 999999)
            cache.set(f'verification_code_email_{user.email}', verification_code_email, timeout=600)
            cache.set(f'verification_code_phone_{user.phone_number}', verification_code_phone, timeout=600)

            send_verification_email(user.email, verification_code_email)
            send_sms(user.phone_number, verification_code_phone)

            messages.success(request, "Des codes de vérification ont été envoyés.")
            return redirect('verify', method='email', identifier=user.email)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})



def send_verification_email(user_email, code):
    """Envoi d'un e-mail de vérification"""
    subject = "Code de vérification"
    body = f"""
        <h1>Vérification de votre compte</h1>
        <p>Votre code de vérification est : <strong>{code}</strong></p>
        <p>Ce code est valide pendant 10 minutes.</p>
    """
    send_email(subject, user_email, body)
    print(f"Code {code} envoyé à l'adresse {user_email}")


def send_email(subject, to_email, body):
    """ Fonction pour gérer l'envoi d'e-mails """
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail

    try:
        message = Mail(
            from_email="nazimlama4@gmail.com",
            to_emails=to_email,
            subject=subject,
            html_content=body
        )
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        sg.send(message)
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")


@login_required
def home(request):
    """ Vue pour la page d'accueil """
    return render(request, 'home.html')


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


@login_required
def level_one_bureau(request):
    return render(request, 'level_one_bureau.html')


@login_required
def level_two(request):
    return render(request, 'level_two.html')


@login_required
def level_three(request):
    return render(request, 'level_three.html')


def test_email(request):
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
    if request.method == "POST":
        code = random.randint(100000, 999999)
        device = StaticDevice.objects.create(user=request.user, name="Telephone")
        device.token_set.create(token=code)
        send_sms(request.user.phone_number, code)
        messages.info(request, "Un code de verification a été envoyé sur votre tel")
        return redirect('verify_2fa_phone')
    return render(request, 'enable_2fa_phone.html')


@login_required
def verify_2fa_phone(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        device = StaticDevice.objects.filter(user=request.user).first()
        if device and device.token_set.filter(token=code).exists():
            messages.success(request, "L'A2F est activée avec succès.")
            return redirect('home')
        messages.error(request, "Code incorrect. Veuillez réessayer.")
    return render(request, 'verify_2fa_phone.html')

