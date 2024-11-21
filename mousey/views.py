import os
from random import randint
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm


def register(request):
    """ Vue pour gérer l'inscription """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Désactive l'utilisateur jusqu'à vérification
            user.save()

            # Générer un code de vérification
            verification_code = randint(100000, 999999)
            cache.set(f'verification_code_{user.email}', verification_code, timeout=600)  # Code valide 10 min

            # Envoyer le code par e-mail
            send_verification_email(user.email, verification_code)

            messages.success(request, "Un code de vérification a été envoyé à votre adresse email.")
            return redirect('verify_email', email=user.email)
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

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

def verify_email(request, email):
    """ Vue pour vérifier le code d'activation """
    if request.method == 'POST':
        code = request.POST.get('code')
        stored_code = cache.get(f'verification_code_{email}')

        if str(code) == str(stored_code):
            user = User.objects.get(email=email)
            user.is_active = True  # Active l'utilisateur
            user.save()
            cache.delete(f'verification_code_{email}')  # Supprime le code du cache

            messages.success(request, "Votre compte a été vérifié avec succès. Vous pouvez vous connecter.")
            return redirect('home')  # Redirection vers home
        else:
            messages.error(request, "Code de vérification incorrect ou expiré.")
    return render(request, 'verify_email.html', {'email': email})


def send_verification_email(user_email, code):
    """ Fonction pour envoyer un e-mail de vérification """
    subject = "Code de vérification"
    body = f"""
        <h1>Vérification de votre compte</h1>
        <p>Votre code de vérification est : <strong>{code}</strong></p>
        <p>Ce code est valide pendant 10 minutes.</p>
    """
    send_email(subject, user_email, body)


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