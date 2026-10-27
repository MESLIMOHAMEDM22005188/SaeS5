from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import RegistrationForm
from .models import (
    EmailVerification,
    FortressGame,
    PhoneVerification,
    LevelOneQuestion,
    LevelThreeQuestion,
    LevelTwoQuestion,
    LevelOneResult,
    LevelThreeResult,
    LevelTwoResult,
)


@login_required
def submit_level_one_quiz(request):
    questions = LevelOneQuestion.objects.prefetch_related("reponses_level_one").order_by("numero")
    if request.method != "POST":
        return render(request, "level_one_quiz.html", {"questions": questions})
    score = 0
    total_questions = questions.count()

    for question in questions:
        correct_answer = next(
            (answer for answer in question.reponses_level_one.all() if answer.est_correcte),
            None,
        )
        selected_answer_id = (request.POST.get(f"q{question.id}") or "").strip()
        if correct_answer and selected_answer_id == str(correct_answer.id):
            score += 1

    LevelOneResult.objects.create(utilisateur=request.user.username, score=score)
    messages.success(request, f"Your score: {score}/{total_questions}.")
    return redirect("quiz_result")


@login_required
def level_one_quiz(request):
    questions = list(
        LevelOneQuestion.objects.prefetch_related("reponses_level_one").order_by("numero")
    )
    total_questions = len(questions)

    if not total_questions:
        messages.info(request, "No quiz questions are available yet.")
        return redirect("home")

    if request.GET.get("restart") == "1":
        request.session.pop("quiz_score", None)
        request.session.pop("quiz_total", None)
        request.session.pop("quiz_answers", None)

    try:
        current_index = int(request.GET.get("q", 0))
    except (TypeError, ValueError):
        current_index = 0
    current_index = max(0, min(current_index, total_questions - 1))
    answers = request.session.get("quiz_answers", {})

    if request.method == "POST":
        question = questions[current_index]
        selected_answer = (request.POST.get("answer") or "").strip()
        valid_answer_ids = {str(answer.id) for answer in question.reponses_level_one.all()}

        if selected_answer in valid_answer_ids:
            answers[str(question.id)] = selected_answer
            request.session["quiz_answers"] = answers

        if "next" in request.POST:
            current_index = min(current_index + 1, total_questions - 1)
        elif "prev" in request.POST:
            current_index = max(current_index - 1, 0)
        elif "finish" in request.POST:
            score = 0
            for quiz_question in questions:
                correct_answer = next(
                    (
                        answer
                        for answer in quiz_question.reponses_level_one.all()
                        if answer.est_correcte
                    ),
                    None,
                )
                if (
                    correct_answer
                    and answers.get(str(quiz_question.id)) == str(correct_answer.id)
                ):
                    score += 1

            LevelOneResult.objects.create(
                utilisateur=request.user.username,
                score=score,
            )
            request.session["quiz_score"] = score
            request.session["quiz_total"] = total_questions
            request.session.pop("quiz_answers", None)
            return redirect("quiz_result")

        return redirect(f"{request.path}?q={current_index}")

    if (
        request.session.get("quiz_total") is not None
        and request.session.get("quiz_score") is not None
    ):
        return redirect("quiz_result")

    return render(
        request,
        "quiz_question.html",
        {
            "question": questions[current_index],
            "current_index": current_index,
            "total_questions": total_questions,
            "selected_answer": answers.get(str(questions[current_index].id)),
            "is_first_question": current_index == 0,
            "is_last_question": current_index == total_questions - 1,
            "progress_percent": round((current_index + 1) / total_questions * 100),
        },
    )



@login_required
def quiz_result(request):
    score = request.session.get("quiz_score")
    total_questions = request.session.get("quiz_total")
    if score is None or total_questions is None:
        return redirect("level_one_quiz")
    return render(
        request,
        "quiz_result.html",
        {"score": score, "total_questions": total_questions},
    )

def login_view(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.error(request, "Invalid username or password.")
        elif not user.is_active:
            messages.error(request, "Your account is not active. Complete email verification first.")
        else:
            auth_login(request, user)
            messages.success(request, "You are now signed in.")
            return redirect("home")

    return render(request, "registration/login.html")


def send_verification_email(user):
    verification, _ = EmailVerification.objects.get_or_create(
        user=user,
        defaults={"email": user.email},
    )
    verification.email = user.email
    verification.generate_code()
    send_mail(
        subject="Verify your email address",
        message=f"Your verification code is: {verification.verification_code}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )


def send_verification_sms(phone_number, code):
    if not all(
        (
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
            settings.TWILIO_PHONE_NUMBER,
        )
    ):
        return False

    try:
        from twilio.rest import Client

        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f"Your verification code is: {code}",
            from_=settings.TWILIO_PHONE_NUMBER,
            to=phone_number,
        )
        return True
    except Exception:
        # Do not log provider errors or verification codes.
        return False


def verify_email_code(request):
    pending_user_id = request.session.get("pending_verification_user_id")
    if not pending_user_id:
        messages.error(request, "Verify your phone number before verifying your email.")
        return redirect("register")

    if request.method != "POST":
        return render(request, "verify_email.html")

    code = (request.POST.get("code") or "").strip()
    verification = (
        EmailVerification.objects.filter(
            user_id=pending_user_id,
            verification_code=code,
            is_verified=False,
        )
        .select_related("user")
        .first()
    )

    if not verification or not verification.is_code_valid():
        messages.error(request, "The verification code is invalid or has expired.")
        return render(request, "verify_email.html", status=400)

    verification.is_verified = True
    verification.verification_code = None
    verification.save(update_fields=["is_verified", "verification_code", "updated_at"])

    user = verification.user
    user.is_active = True
    user.save(update_fields=["is_active"])
    request.session.pop("pending_verification_user_id", None)
    messages.success(request, "Email verified. You can now sign in.")
    return redirect("login")


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
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

            sms_sent = send_verification_sms(
                phone_number,
                phone_verification.verification_code,
            )
            try:
                send_verification_email(user)
            except Exception:
                messages.error(request, "Email delivery failed. Check the SMTP configuration.")
                return render(request, "registration.html", {"form": form}, status=503)

            if not sms_sent:
                messages.warning(
                    request,
                    "SMS delivery is not configured. The account will remain inactive until phone verification.",
                )
            messages.success(request, "Check your phone and email to activate your account.")
            return redirect("verify_phone", identifier=user.username)

        messages.error(request, "Please correct the errors in the registration form.")
    else:
        form = RegistrationForm()

    return render(request, "registration.html", {"form": form})


def verify_phone_code(request, identifier):
    user = get_user_model().objects.filter(username=identifier).first()
    if user is None:
        messages.error(request, "Account not found.")
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
            and verification.code_expiration > timezone.now()
        ):
            verification.is_verified = True
            verification.verification_code = None
            verification.save(
                update_fields=["is_verified", "verification_code", "updated_at"]
            )
            request.session["pending_verification_user_id"] = user.pk
            messages.success(request, "Phone number verified.")
            return redirect("verify_email")

        messages.error(request, "The verification code is invalid or has expired.")

    return render(request, "verify.html", {"identifier": identifier})


def dashboard(request):
    return render(request, "home.html")


@login_required
def phishing_warning(request):
    return render(request, "screen_warning.html")


@login_required
def level_one_intro(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        # This is a phishing-awareness simulation, not a real login endpoint.
        if username and password:
            messages.info(
                request,
                "Simulation: never enter real credentials on an untrusted page.",
            )
            return redirect("phishing_warning")
        messages.error(request, "Enter both fields to run the simulation.")

    return render(request, "level_one.html")


@login_required
def submit_level_two_quiz(request):
    questions = list(
        LevelTwoQuestion.objects.prefetch_related("reponses_level_two").order_by("numero")
    )
    if request.method == "POST":
        score = 0
        for question in questions:
            selected_id = (request.POST.get(f"q{question.id}") or "").strip()
            correct_answer = next(
                (
                    answer
                    for answer in question.reponses_level_two.all()
                    if answer.est_correcte
                ),
                None,
            )
            if correct_answer and selected_id == str(correct_answer.id):
                score += 1

        LevelTwoResult.objects.create(utilisateur=request.user.username, score=score)
        messages.success(request, f"Your score: {score}/{len(questions)}.")
        return redirect("level_two_quiz")

    return render(request, "level_two_quiz.html", {"questions": questions})


@login_required
def level_one_desktop(request):
    return render(request, "level_one_desktop.html")


@login_required
def level_two_game_one(request):
    return render(request, "level_two_game_one.html")


@login_required
def submit_level_three_quiz(request):
    questions = list(
        LevelThreeQuestion.objects.prefetch_related("reponses").order_by("numero")
    )
    if request.method == "POST":
        score = 0
        for question in questions:
            selected_id = (request.POST.get(f"q{question.id}") or "").strip()
            correct_answer = next(
                (answer for answer in question.reponses.all() if answer.est_correcte),
                None,
            )
            if correct_answer and selected_id == str(correct_answer.id):
                score += 1

        LevelThreeResult.objects.create(utilisateur=request.user.username, score=score)
        messages.success(request, f"Your score: {score}/{len(questions)}.")
        return redirect("level_three_quiz")

    return render(request, "level_three_quiz.html", {"questions": questions})


@login_required
def save_password_game_result(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed."}, status=405)

    # Only persist the non-sensitive game state, never the submitted password.
    password = (request.POST.get("password") or "").strip()
    strength = (request.POST.get("strength") or "weak").strip().lower()
    if not password:
        return JsonResponse({"error": "A password is required."}, status=400)

    if strength not in {"weak", "medium", "strong"}:
        return JsonResponse({"error": "Invalid password strength."}, status=400)

    FortressGame.objects.create(user=request.user, password="", strength=strength)
    return JsonResponse({"message": "Game progress saved."}, status=201)


@login_required
def level_two_game_two(request):
    return render(request, "level_two_game_two.html")


@login_required
def level_two_dashboard(request):
    return render(request, "level_two.html")


@login_required
def level_three_dashboard(request):
    return render(request, "level_three.html")


@login_required
def password_game(request):
    return render(request, "password_game.html")


@login_required
def level_two_lesson(request):
    return render(request, "level_two_lesson.html")


@login_required
def level_two_game_three(request):
    return render(request, "level_two_game_three.html")


@login_required
def level_two_game_four(request):
    return render(request, "level_two_game_four.html")


@login_required
def browser_simulation(request):
    return render(request, "browser_simulation.html")
