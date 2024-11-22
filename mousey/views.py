import random
from random import randint

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from python_http_client import Client

from .forms import UserCreationFormWithFields


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



def send_verification_sms(phone_number, code):
    """Envoi d'un SMS de vérification."""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=f"Votre code de vérification est : {code}. Ce code est valide pendant 10 minutes.",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number,
        )
    except Exception as e:
        print(f"Erreur lors de l'envoi du SMS : {e}")




def register(request):
    """Vue pour l'enregistrement utilisateur."""
    if request.method == 'POST':
        form = UserCreationFormWithFields(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            phone_number = request.POST.get('phone_number')
            verification_code = randint(100000, 999999)
            cache.set(f'verification_code_phone_{phone_number}', verification_code, timeout=600)

            send_verification_sms(phone_number, verification_code)
            messages.success(request, "Un code de vérification a été envoyé à votre numéro de téléphone.")
            return redirect('verify', identifier=phone_number)
    else:
        form = UserCreationFormWithFields()

    return render(request, 'register.html', {'form': form})

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
        stored_code = cache.get(f'verification_code_phone_{identifier}')

        if stored_code and str(code) == str(stored_code):
            user = get_user_model().objects.filter(username=identifier).first()
            if user:
                user.is_active = True
                user.save()
                cache.delete(f'verification_code_phone_{identifier}')
                auth_login(request, user)
                messages.success(request, "Votre compte a été vérifié avec succès.")
                return redirect('home')
            else:
                messages.error(request, "Utilisateur non trouvé.")
        else:
            messages.error(request, "Code incorrect ou expiré.")
    return render(request, 'verify.html', {'identifier': identifier})


#@login_required
def home(request):
    """Page d'accueil."""
    return render(request, 'home.html')


#@login_required
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


#@login_required
def level_one_bureau(request):
    """Page pour le bureau du niveau 1."""
    return render(request, 'level_one_bureau.html')


#@login_required
def level_two(request):
    """Page pour le niveau 2."""
    return render(request, 'level_two.html')


#@login_required
def level_three(request):
    """Page pour le niveau 3."""
    return render(request, 'level_three.html')
