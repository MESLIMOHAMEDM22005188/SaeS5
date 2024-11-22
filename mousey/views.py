from random import randint

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.utils.timezone import now
from python_http_client import Client

from .forms import  UserCreationFormWithPhone
from .models import PhoneVerification


def user_login(request):
    """Vue pour la connexion utilisateur."""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_active:
                messages.error(request, "Votre compte n'est pas activé. Veuillez vérifier votre e-mail.")
            else:
                auth_login(request, user)
                messages.success(request, "Connexion réussie !")
                return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'registration/login.html')

def register(request):
    """Vue pour l'enregistrement utilisateur."""
    if request.method == 'POST':
        form = UserCreationFormWithPhone(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                phone_number = form.cleaned_data['phone_number']

                # Créer une entrée dans la table PhoneVerification
                phone_verification, created = PhoneVerification.objects.get_or_create(user=user, phone_number=phone_number)

                # Générer et envoyer le code de vérification
                verification_code = send_verification_sms(phone_number)
                if verification_code:
                    phone_verification.verification_code = verification_code
                    phone_verification.save()

                    messages.success(request, "Un code de vérification a été envoyé à votre téléphone.")
                    return redirect('verify', identifier=user.username)
                else:
                    messages.error(request, "Erreur lors de l'envoi du code. Veuillez réessayer.")
            except Exception as e:
                messages.error(request, f"Une erreur inattendue s'est produite : {e}")
        else:
            messages.error(request, "Formulaire invalide. Veuillez vérifier vos informations.")
    else:
        form = UserCreationFormWithPhone()

    return render(request, 'register.html', {'form': form})


def send_verification_sms(phone_number):
    """Envoi d'un SMS de vérification avec un code à un utilisateur."""
    # Twilio credentials
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    # Générer un code de vérification
    verification_code = randint(100000, 999999)

    # Message à envoyer
    message_body = f"Votre code de vérification est : {verification_code}. Ce code est valide pendant 10 minutes."

    try:
        # Envoi du SMS
        message = client.messages.create(
            body=message_body,
            from_="+1 904 637 7917",  # Numéro Twilio
            to=phone_number            # Numéro de l'utilisateur
        )
        print(f"Message envoyé avec SID: {message.sid}")

        return verification_code
    except Exception as e:
        print(f"Erreur lors de l'envoi du SMS : {e}")
        return None

"""
def send_email(subject, to_email, body):
    Envoi d'un e-mail via Django SendMail.
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[to_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")
    


def send_verification_email(user_email, code):
    "Envoi d'un e-mail de vérification.
    subject = "Code de vérification"
    body = f"Votre code de vérification est : {code}. Ce code est valide pendant 10 minutes."
    send_email(subject, user_email, body)
"""

def verify(request, identifier):
    """Vérification du compte utilisateur via un code envoyé par SMS."""
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            phone_verification = PhoneVerification.objects.get(user__username=identifier)
            if phone_verification.verification_code == code:
                phone_verification.is_verified = True
                phone_verification.save()

                user = phone_verification.user
                user.is_active = True
                user.save()

                auth_login(request, user)
                messages.success(request, "Votre compte a été vérifié avec succès.")
                return redirect('home')
            else:
                messages.error(request, "Code incorrect ou expiré.")
        except PhoneVerification.DoesNotExist:
            messages.error(request, "Vérification impossible. Veuillez vous inscrire à nouveau.")
    return render(request, 'verify.html', {'identifier': identifier})
@login_required
def home(request):
    """Page d'accueil."""
    return render(request, 'home.html')


@login_required
def level_one(request):
    """Page pour le niveau 1."""
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
    """Page pour le bureau du niveau 1."""
    return render(request, 'level_one_bureau.html')


@login_required
def level_two(request):
    """Page pour le niveau 2."""
    return render(request, 'level_two.html')


@login_required
def level_three(request):
    """Page pour le niveau 3."""
    return render(request, 'level_three.html')
