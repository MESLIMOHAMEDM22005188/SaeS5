from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
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
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre compte a été créé avec succès !')
            return redirect('login')
    else:
        form = UserCreationForm()

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
