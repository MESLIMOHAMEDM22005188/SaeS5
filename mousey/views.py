from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.core.mail import send_mail
from .forms import UserCreationFormWithPhone
from .models import (EmailVerification, PhoneVerification, QuestionLevelOne, ResultatLevelOne, Forteresse, QuestionLevelThree, QuestionLevelTwo, ResultatLevelThree, ResultatLevelTwo, ReponseLevelThree, ReponseLevelTwo)

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
    """Run the level-one quiz one question at a time and persist the final score."""
    questions = list(QuestionLevelOne.objects.prefetch_related("reponses_level_one").order_by("numero"))
    total_questions = len(questions)

    if total_questions == 0:
        messages.info(request, "Aucune question n'est disponible pour le moment.")
        return redirect("home")

    try:
        current_index = int(request.GET.get("q", 0))
    except (TypeError, ValueError):
        current_index = 0
    current_index = max(0, min(current_index, total_questions - 1))

    answers = request.session.get("quiz_answers", {})

    if request.method == "POST":
        current_question = questions[current_index]
        selected_answer = (request.POST.get("answer") or "").strip()
        valid_answer_ids = {str(answer.id) for answer in current_question.reponses_level_one.all()}
        if selected_answer and selected_answer in valid_answer_ids:
            answers[str(current_question.id)] = selected_answer
            request.session["quiz_answers"] = answers

        if "next" in request.POST:
            current_index = min(current_index + 1, total_questions - 1)
        elif "prev" in request.POST:
            current_index = max(current_index - 1, 0)
        elif "finish" in request.POST:
            score = 0
            for question in questions:
                correct = next(
                    (answer for answer in question.reponses_level_one.all() if answer.est_correcte),
                    None,
                )
                if correct and answers.get(str(question.id)) == str(correct.id):
                    score += 1
            ResultatLevelOne.objects.create(utilisateur=request.user.username, score=score)
            request.session["quiz_score"] = score
            request.session["quiz_total"] = total_questions
            request.session.pop("quiz_answers", None)
            return redirect("quiz_result")

        return redirect(f"{request.path}?q={current_index}")

    if request.session.get("quiz_total") is not None and request.session.get("quiz_score") is not None:
        return render(
            request,
            "quiz_result.html",
            {
                "score": request.session["quiz_score"],
                "total_questions": request.session["quiz_total"],
            },
        )

    return render(
        request,
        "quiz_question.html",
        {
            "question": questions[current_index],
            "current_index": current_index,
            "total_questions": total_questions,
            "selected_answer": answers.get(str(questions[current_index].id)),
        },
    )

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


def send_verification_email(user):
    """Create and send an expiring verification code to the given user."""
    verification, _ = EmailVerification.objects.get_or_create(
        user=user,
        defaults={"email": user.email},
    )
    verification.email = user.email
    verification.generate_code()
    send_mail(
        subject="Vérification de votre adresse e-mail",
        message=f"Votre code de vérification est : {verification.verification_code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_verification_sms(phone_number, code):
    """Send an SMS verification code when Twilio is configured."""
    if not all((settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_PHONE_NUMBER)):
        return False

    try:
        from twilio.rest import Client as TwilioClient

        client = TwilioClient(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f"Votre code de vérification est : {code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number,
        )
        return True
    except Exception:
        # Avoid logging provider details or verification codes.
        return False


def verify_email(request):
    pending_user_id = request.session.get("pending_verification_user_id")
    if not pending_user_id:
        messages.error(request, "Commencez par vérifier le numéro de téléphone associé à votre compte.")
        return redirect("register")

    if request.method != "POST":
        return render(request, "verify_email.html")

    code = (request.POST.get("code") or "").strip()
    verification = EmailVerification.objects.filter(
        user_id=pending_user_id,
        verification_code=code,
        is_verified=False,
    ).select_related("user").first()

    if not verification or not verification.is_code_valid():
        messages.error(request, "Code invalide ou expiré.")
        return render(request, "verify_email.html", status=400)

    verification.is_verified = True
    verification.verification_code = None
    verification.save(update_fields=["is_verified", "verification_code", "updated_at"])
    user = verification.user
    user.is_active = True
    user.save(update_fields=["is_active"])
    request.session.pop("pending_verification_user_id", None)
    messages.success(request, "Votre adresse e-mail a été vérifiée. Vous pouvez vous connecter.")
    return redirect("login")


def register(request):
    """Create an inactive account and start the phone/e-mail verification flow."""
    if request.method == "POST":
        form = UserCreationFormWithPhone(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            phone_number = form.cleaned_data["phone_number"]
            email = form.cleaned_data["email"]

            phone_verification = PhoneVerification.objects.create(
                user=user,
                phone_number=phone_number,
            )
            email_verification, _ = EmailVerification.objects.get_or_create(
                user=user,
                defaults={"email": email},
            )
            phone_verification.generate_code()
            email_verification.email = email
            email_verification.generate_code()
            sms_sent = send_verification_sms(phone_number, phone_verification.verification_code)
            try:
                send_verification_email(user)
            except Exception:
                messages.error(request, "L'envoi de l'e-mail a échoué. Vérifiez la configuration SMTP.")
                return render(request, "register.html", {"form": form}, status=503)

            if not sms_sent:
                messages.warning(request, "SMS non configuré : le compte reste désactivé jusqu'à validation du téléphone.")
            messages.success(request, "Vérifiez votre téléphone puis votre adresse e-mail pour activer le compte.")
            return redirect("verify", identifier=user.username)
        messages.error(request, "Erreur dans le formulaire. Veuillez vérifier vos informations.")
    else:
        form = UserCreationFormWithPhone()
    return render(request, "register.html", {"form": form})


def verify(request, identifier):
    """Verify the phone code associated with the requested account."""
    user = get_user_model().objects.filter(username=identifier).first()
    if not user:
        messages.error(request, "Utilisateur introuvable.")
        return redirect("register")

    if request.method == "POST":
        code = (request.POST.get("code") or "").strip()
        verification = PhoneVerification.objects.filter(user=user).first()
        if (
            verification
            and not verification.is_verified
            and verification.verification_code
            and verification.verification_code == code
            and verification.code_expiration
            and verification.code_expiration > now()
        ):
            verification.is_verified = True
            verification.verification_code = None
            verification.save(update_fields=["is_verified", "verification_code", "updated_at"])
            request.session["pending_verification_user_id"] = user.pk
            messages.success(request, "Votre numéro a été vérifié.")
            return redirect("verify_email")
        messages.error(request, "Code incorrect ou expiré.")

    return render(request, "verify.html", {"identifier": identifier})


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
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        # This screen is a phishing-awareness simulation, not a real login endpoint.
        if username and password:
            messages.info(request, "Simulation : ne saisis jamais tes identifiants sur une page non fiable.")
            return redirect("screen_warning")
        messages.error(request, "Renseigne les deux champs pour lancer la simulation.")
    return render(request, 'level_one.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import QuestionLevelTwo, ResultatLevelTwo

@login_required
def test_level2_view(request):
    questions = list(QuestionLevelTwo.objects.prefetch_related("reponses_level_two").order_by("numero"))
    if request.method == "POST":
        score = 0
        for question in questions:
            selected_id = (request.POST.get(f"q{question.id}") or "").strip()
            correct = next((answer for answer in question.reponses_level_two.all() if answer.est_correcte), None)
            if selected_id and correct and selected_id == str(correct.id):
                score += 1
        ResultatLevelTwo.objects.create(utilisateur=request.user.username, score=score)
        messages.success(request, f"Vous avez obtenu {score}/{len(questions)} bonne(s) réponse(s) !")
        return redirect("level_two_quizz")

    return render(request, "test_level2.html", {"questions": questions})

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
    questions = list(QuestionLevelThree.objects.prefetch_related("reponses").order_by("numero"))
    if request.method == "POST":
        score = 0
        for question in questions:
            selected_id = (request.POST.get(f"q{question.id}") or "").strip()
            correct = next((answer for answer in question.reponses.all() if answer.est_correcte), None)
            if selected_id and correct and selected_id == str(correct.id):
                score += 1
        ResultatLevelThree.objects.create(utilisateur=request.user.username, score=score)
        messages.success(request, f"Vous avez obtenu {score}/{len(questions)} bonne(s) réponse(s) !")
        return redirect("level_three_quizz")

    return render(request, "test_level3.html", {"questions": questions})

def save_password(request):
    """Store game progress without persisting the user's plaintext password."""
    if request.method != "POST":
        return JsonResponse({"error": "Méthode non autorisée."}, status=405)

    password = (request.POST.get("password") or "").strip()
    strength = (request.POST.get("strength") or "weak").strip().lower()

    if not password:
        return JsonResponse({"error": "Le mot de passe est obligatoire."}, status=400)

    allowed_strengths = {"weak", "medium", "strong"}
    if strength not in allowed_strengths:
        return JsonResponse({"error": "Niveau de robustesse invalide."}, status=400)

    # Do not store plaintext passwords: keep only a non-sensitive game state.
    Forteresse.objects.create(
        user=request.user,
        password="",
        strength=strength,
    )
    return JsonResponse({"message": "Progression enregistrée."}, status=201)

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

#vue pour la page du navigateur internet du premier niveau.
def browser_level_one(request):
    return render(request, 'test.html')
