from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect

from mickey.settings import send_email
from .forms import CustomUserCreationForm
from mousey.forms import CustomUserCreationForm
from django.contrib.auth.models import User


@login_required
def level_one(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Vérifie l'identifiant et le mot de passe
        if username == "utilisateur4" and password == "01234":
            return redirect('level_one_bureau')
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect.")

    return render(request, 'level_one.html')


@login_required
def level_two(request):
    return render(request, 'level_two.html')


@login_required
def level_three(request):
    return render(request, 'level_three.html')


@login_required
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)  # Utilisation du formulaire personnalisé
        if form.is_valid():
            user = form.save()
            # Envoi d'e-mail de bienvenue
            send_email(
                subject="Bienvenue sur notre plateforme !",
                to_emails=user.email,  # Utilisation de l'e-mail saisi par l'utilisateur
                body=f"""
                    <h1>Bonjour {user.username},</h1>
                    <p>Merci de vous être inscrit sur notre site. Nous espérons que vous apprécierez votre expérience.</p>
                    <p>Cordialement,</p>
                    <p>L'équipe</p>
                """
            )
            messages.success(request, 'Votre compte a été créé avec succès ! Un e-mail de bienvenue vous a été envoyé.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})
@login_required
def level_one_bureau(request):
    return render(request, 'level_one_bureau.html')


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
