import re
import uuid
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.management import BaseCommand
from django.shortcuts import render, redirect
from django.utils.timezone import now
from python_http_client import Client
from django.core.mail import send_mail
from django_ratelimit.decorators import ratelimit
from .forms import UserCreationFormWithPhone
from .models import PhoneVerification, EmailVerification
from .models import QuestionLevelOne, ResultatLevelOne, ReponseLevelOne


@login_required
def test_level1_view(request):
    if request.method == "POST":
        # Récupérer les réponses soumises par l'utilisateur
        user_answers = request.POST

        # Calculer le score
        questions = QuestionLevelOne.objects.all().order_by('numero')
        score = 0
        total_questions = questions.count()

        for question in questions:
            # Obtenir la réponse correcte pour la question
            correct_answer = question.reponses.filter(est_correcte=True).first()

            # Comparer avec la réponse de l'utilisateur
            user_answer_id = user_answers.get(f'q{question.id}')
            if user_answer_id and str(correct_answer.id) == user_answer_id:
                score += 1

        # Sauvegarder le résultat en base
        ResultatLevelOne.objects.create(utilisateur=request.user.username, score=score)

        # Afficher un message de résultat et rediriger
        messages.success(request, f"Vous avez obtenu {score}/{total_questions} bonne(s) réponse(s) !")
        return redirect('test_level1')

    # Si ce n'est pas une requête POST, afficher les questions
    questions = QuestionLevelOne.objects.all().order_by('numero')
    return render(request, 'test_level1.html', {'questions': questions})


@ratelimit(key='ip', rate='5/m', block=True)
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


def envoyer_email():
    send_mail(
        subject="test email",
        message="Ceci est un test envoyé via AlwaysData",
        from_email="cybermouse@alwaysdata.net",
        recipient_list=["pacmanthebossofhack@gmail.com"],
        fail_silently=False,
    )


def send_verification_email(user):
    code = uuid.uuid4().hex[:6].upper()
    email_verification, created = EmailVerification.objects.get_or_create(
        user=user,
        defaults={
            "email": user.email,
            "verification_code": code,
        }
    )
    if not created:
        email_verification.verification_code = code
        email_verification.save()

    send_mail(
        subject="Vérification de votre adresse e-mail",
        message=f"Votre code de vérification est : {code}",
        from_email="cybermouse@alwaysdata.net",
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_verification_sms(phone_number, code):
    """Envoi d'un SMS de vérification."""
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        client.messages.create(
            body=f"Votre code de vérification est: {code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number,
        )
    except Exception as e:
        print(f"Erreur lors de l'envoi du SMS: {e}")


def verify_email(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        email_verification = EmailVerification.objects.filter(verification_code=code).first()
        if email_verification:
            email_verification.is_verified = True
            email_verification.save()
            return redirect('home')
        else:
            messages.error(request, "Code invalide.")
    return render(request, 'verify_email.html')

def register(request):
    """Vue pour enregistrer un utilisateur et ajouter un numéro de téléphone et un email."""
    if request.method == 'POST':
        form = UserCreationFormWithPhone(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']

            phone_verification = PhoneVerification.objects.create(
                user=user,
                phone_number=phone_number
            )
            email_verification = EmailVerification.objects.create(
                user=user,
                email=email
            )
            phone_verification.generate_code()
            email_verification.generate_code()

            send_verification_sms(phone_number, phone_verification.verification_code)

            send_verification_email(user)

            messages.success(
                request,
                "Un code de vérification a été envoyé à votre téléphone et à votre adresse e-mail."
            )
            return redirect('verify', identifier=user.username)
        else:
            messages.error(request, "Erreur dans le formulaire. Veuillez vérifier vos informations.")
    else:
        form = UserCreationFormWithPhone()

    return render(request, 'register.html', {'form': form})


def verify(request, identifier):
    """Vérification du compte via un code SMS."""
    user = get_user_model().objects.filter(username=identifier).first()
    if not user:
        messages.error(request, "Utilisateur introuvable.")
        return redirect('register')

    if request.method == 'POST':
        code = request.POST.get('code')
        phone_verification = PhoneVerification.objects.filter(user=user).first()

        if phone_verification and phone_verification.verification_code == code:
            if phone_verification.code_expiration > now():
                phone_verification.is_verified = True
                phone_verification.save()
                messages.success(request, "Votre numéro a été vérifié avec succès.")
                return redirect('verify_email')  # Redirige vers la vérification de l'email
            else:
                messages.error(request, "Le code a expiré.")
        else:
            messages.error(request, "Code incorrect.")

    return render(request, 'verify.html', {'identifier': identifier})

@login_required
def home(request):
    """Page d'accueil."""
    return render(request, 'home.html')

@login_required
def screen_warning(request):
    """Affiche un écran noir avec un message de sensibilisation."""
    return render(request, 'screen_warning.html')

@login_required
def level_one(request):
    """Page pour le niveau 1."""
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == "utilisateur4" and password == "01234":
            return redirect('screen_warning')
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

#vue pour la page du navigateur internet du premier niveau.
def browser_level_one(request):
    return render(request, 'browser.html')


class Command(BaseCommand):
    help = 'Supprime les codes de vérification expirés'

    def handle(self, *args, **kwargs):
        EmailVerification.objects.filter(code_expiration__lt=now()).delete()
        PhoneVerification.objects.filter(code_expiration__lt=now()).delete()
        self.stdout.write("Codes expirés supprimés.")
