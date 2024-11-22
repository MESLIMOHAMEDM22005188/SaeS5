import random
from random import randint
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import UserCreationFormWithFields


def user_login(request):
    """Vue pour la connexion utilisateur."""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if not user.is_active:
                messages.error(request, "Votre compte n'est pas activé. Veuillez vérifier votre e-mail.")
            else:
                login(request, user)
                messages.success(request, "Connexion réussie !")
                return redirect('home')
        else:
            messages.error(request, "Nom d'utilisateur ou mot de passe incorrect.")
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationFormWithFields(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            verification_code_email = randint(100000, 999999)
            cache.set(f'verification_code_email_{user.email}', verification_code_email, timeout=600)

            send_verification_email(user.email, verification_code_email)
            messages.success(request, "Un code de vérification a été envoyé à votre adresse e-mail.")

            # Redirection vers la page de vérification
            return redirect('verify', identifier=user.email)

    else:
        form = UserCreationFormWithFields()

    return render(request, 'register.html', {'form': form})
def send_email(subject, to_email, body):
    """Envoi d'un e-mail via Django SendMail."""
    try:
        send_mail(
            subject=subject,
            message=body,
            from_email=None,  # Utilisera DEFAULT_FROM_EMAIL dans settings.py
            recipient_list=[to_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'e-mail : {e}")


def send_verification_email(user_email, code):
    """Envoi d'un e-mail de vérification."""
    subject = "Code de vérification"
    body = f"""
        Votre code de vérification est : {code}.
        Ce code est valide pendant 10 minutes.
    """
    send_email(subject, user_email, body)


#@login_required
def home(request):
    """Page d'accueil."""
    return render(request, 'home.html')

def verify(request, identifier):
    """Vérification du compte utilisateur via un code envoyé par e-mail."""
    if request.method == 'POST':
        code = request.POST.get('code')
        stored_code = cache.get(f'verification_code_email_{identifier}')

        if stored_code and str(code) == str(stored_code):
            user = get_user_model().objects.filter(email=identifier).first()
            if user:
                user.is_active = True
                user.save()
                cache.delete(f'verification_code_email_{identifier}')
                login(request, user)  # Connecte l'utilisateur automatiquement
                messages.success(request, "Votre compte a été vérifié avec succès et vous êtes maintenant connecté.")
                return redirect('home')
            else:
                messages.error(request, "Utilisateur non trouvé.")
        else:
            messages.error(request, "Code incorrect ou expiré. Veuillez réessayer.")

    return render(request, 'verify.html', {'identifier': identifier})
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
