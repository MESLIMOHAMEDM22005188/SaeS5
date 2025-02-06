import re
import uuid
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.management import BaseCommand
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from python_http_client import Client
from django.core.mail import send_mail
from django_ratelimit.decorators import ratelimit
from .forms import UserCreationFormWithPhone
from .models import PhoneVerification, EmailVerification
from .models import QuestionLevelOne, ResultatLevelOne, Forteresse, QuestionLevelThree, QuestionLevelTwo,ResultatLevelThree, ResultatLevelTwo, ReponseLevelThree, ReponseLevelTwo

from django.shortcuts import render

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
            # Utilisez le related_name correct : 'reponses_level_one'
            correct_answer = question.reponses_level_one.filter(est_correcte=True).first()

            # Comparer avec la réponse de l'utilisateur
            user_answer_id = user_answers.get(f'q{question.id}')
            if user_answer_id and correct_answer and str(correct_answer.id) == user_answer_id:
                score += 1

        # Sauvegarder le résultat en base, afficher un message, etc.
        ResultatLevelOne.objects.create(utilisateur=request.user.username, score=score)
        messages.success(request, f"Vous avez obtenu {score}/{total_questions} bonne(s) réponse(s) !")
        return redirect('level_one_quizz')

    # Requête GET : afficher les questions
    questions = QuestionLevelOne.objects.all().order_by('numero')
    return render(request, 'test_level1.html', {'questions': questions})


@login_required
def quiz_result(request):
    # Récupération de toutes les questions triées par numéro
    questions = list(QuestionLevelOne.objects.all().order_by('numero'))
    total_questions = len(questions)

    # Récupérer l'index courant de la question depuis la requête GET (par défaut 0)
    try:
        current_index = int(request.GET.get('q', 0))
    except (ValueError, TypeError):
        current_index = 0

    # Initialiser ou récupérer les réponses stockées dans la session
    if 'quiz_answers' not in request.session:
        request.session['quiz_answers'] = {}
    answers = request.session['quiz_answers']

    if request.method == "POST":
        # Enregistrer la réponse de la question actuelle
        current_question = questions[current_index]
        selected_answer = request.POST.get('answer')
        if selected_answer:
            answers[str(current_question.id)] = selected_answer
            request.session['quiz_answers'] = answers  # Mémoriser dans la session

        # Gestion de la navigation
        if 'next' in request.POST:
            if current_index < total_questions - 1:
                current_index += 1
        elif 'prev' in request.POST:
            if current_index > 0:
                current_index -= 1
        elif 'finish' in request.POST:
            # Calcul du score
            score = 0
            for q in questions:
                # Récupérer la bonne réponse (en supposant qu'il n'y a qu'une bonne réponse par question)
                correct = q.reponses_level_one.filter(est_correcte=True).first()
                # Comparer la réponse enregistrée dans la session (sous forme de chaîne) avec l'ID de la bonne réponse
                if correct and answers.get(str(q.id)) == str(correct.id):
                    score += 1
            # Enregistrer le résultat dans la base de données
            ResultatLevelOne.objects.create(utilisateur=request.user.username, score=score)
            # Stocker le score et le total dans la session pour affichage dans la page résultat
            request.session['quiz_score'] = score
            request.session['quiz_total'] = total_questions
            return redirect('quiz_result')  # Assurez-vous que l'URL 'quiz_result' est bien définie dans urls.py

        # Rediriger vers la même vue en passant le nouvel index dans l'URL
        return redirect(f"{request.path}?q={current_index}")

    # Pour une requête GET, afficher la question à l'index courant
    current_question = questions[current_index]
    context = {
        'question': current_question,
        'current_index': current_index,
        'total_questions': total_questions,
    }
    return render(request, 'quiz_question.html', context)

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


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import QuestionLevelTwo, ResultatLevelTwo

@login_required
def test_level2_view(request):
    if request.method == "POST":
        user_answers = request.POST
        questions = QuestionLevelTwo.objects.all().order_by('numero')
        score = 0
        total_questions = questions.count()

        for question in questions:
            # Ici, on parcourt les réponses du niveau 2 via le related_name 'reponses'
            correct_answer = question.reponses.filter(est_correcte=True).first()
            user_answer_id = user_answers.get(f'q{question.id}')
            if user_answer_id and str(correct_answer.id) == user_answer_id:
                score += 1

        # Sauvegarde du résultat pour le niveau 2
        ResultatLevelTwo.objects.create(utilisateur=request.user.username, score=score)
        messages.success(request, f"Vous avez obtenu {score}/{total_questions} bonne(s) réponse(s) !")
        return redirect('test_level2')  # Assurez-vous que l'URL 'test_level2' est bien définie

    else:
        questions = QuestionLevelTwo.objects.all().order_by('numero')
        return render(request, 'test_level2.html', {'questions': questions})



@login_required
def level_one_bureau(request):
    """Page pour le bureau du niveau 1."""
    return render(request, 'level_one_bureau.html')

@login_required
def level_two_jeu1(request):
    """Page pour le niveau 2."""
    return render(request, 'level_twoJeu1.html')
@login_required
def test_level3_view(request):
    if request.method == "POST":
        user_answers = request.POST
        # On récupère les questions du niveau 3
        questions = QuestionLevelThree.objects.all().order_by('numero')
        score = 0
        total_questions = questions.count()

        for question in questions:
            # On parcourt les réponses liées au niveau 3 (grâce au related_name "reponses")
            correct_answer = question.reponses.filter(est_correcte=True).first()
            user_answer_id = user_answers.get(f'q{question.id}')
            if user_answer_id and str(correct_answer.id) == user_answer_id:
                score += 1

        # Enregistrement du résultat dans ResultatLevelThree
        ResultatLevelThree.objects.create(utilisateur=request.user.username, score=score)
        messages.success(request, f"Vous avez obtenu {score}/{total_questions} bonne(s) réponse(s) !")
        return redirect('test_level3')  # Assurez-vous que l'URL 'test_level3' est bien définie

    else:
        questions = QuestionLevelThree.objects.all().order_by('numero')
        return render(request, 'test_level3.html', {'questions': questions})
def save_password(request):
    if request.method == "POST":
       if not request.user.is_authenticated:
           return JsonResponse({'error': 'Authentication required'}, status=401)
    password = request.POST.get('password').strip
    strength = request.POST.get('strength', 'weak')

    Forteresse.objects.create(
        user=request.user,
        password=password,
        strength=strength
    )
    return JsonResponse({'message': 'Mot de passe enregistré avec succès.'})

    return JsonResponse({'error': 'Requête non valide.'}, status=400)

@login_required
def level_two_jeu2(request):
    return render(request, 'level_twoJeu2.html')

@login_required
def level_two(request):
    return render(request, 'level_two.html')

@login_required
def level_three(request):
    return render(request, 'level_three.html')
@login_required
def level_two_pswd(request):
    return render(request, 'level_two_pswd.html')
@login_required
def level_two_course(request):
    return render(request, 'level_two_course.html')

@login_required
def level_two_jeu3(request):
    return render(request, ''
                           'level_twoJeu3.html')
@login_required
def level_two_jeu4(request):
    return render(request, 'level_twoJeu4.html')

@login_required
def level_three(request):
    """Page pour le niveau 3."""
    return render(request, 'level_three.html')

#vue pour la page du navigateur internet du premier niveau.
def browser_level_one(request):
    return render(request, 'test.html')


class Command(BaseCommand):
    help = 'Supprime les codes de vérification expirés'

    def handle(self, *args, **kwargs):
        EmailVerification.objects.filter(code_expiration__lt=now()).delete()
        PhoneVerification.objects.filter(code_expiration__lt=now()).delete()
        self.stdout.write("Codes expirés supprimés.")
