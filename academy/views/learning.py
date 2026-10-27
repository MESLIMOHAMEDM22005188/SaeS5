"""Quiz flows and learning-level pages."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from academy.models import (
    LevelOneQuestion, LevelOneResult, LevelThreeQuestion, LevelThreeResult,
    LevelTwoQuestion, LevelTwoResult,
)


@login_required
def submit_level_one_quiz(request):
    questions = LevelOneQuestion.objects.prefetch_related("reponses_level_one").order_by("numero")
    if request.method != "POST":
        return render(request, "level_one_quiz.html", {"questions": questions})
    score = 0
    total_questions = questions.count()
    for question in questions:
        correct = next((a for a in question.reponses_level_one.all() if a.est_correcte), None)
        selected = (request.POST.get(f"q{question.id}") or "").strip()
        if correct and selected == str(correct.id):
            score += 1
    LevelOneResult.objects.create(utilisateur=request.user.username, score=score)
    messages.success(request, f"Your score: {score}/{total_questions}.")
    return redirect("quiz_result")


@login_required
def level_one_quiz(request):
    questions = list(LevelOneQuestion.objects.prefetch_related("reponses_level_one").order_by("numero"))
    total = len(questions)
    if not total:
        messages.info(request, "No quiz questions are available yet.")
        return redirect("home")
    if request.GET.get("restart") == "1":
        for key in ("quiz_score", "quiz_total", "quiz_answers"):
            request.session.pop(key, None)
    try:
        index = int(request.GET.get("q", 0))
    except (TypeError, ValueError):
        index = 0
    index = max(0, min(index, total - 1))
    answers = request.session.get("quiz_answers", {})
    if request.method == "POST":
        question = questions[index]
        selected = (request.POST.get("answer") or "").strip()
        valid_ids = {str(a.id) for a in question.reponses_level_one.all()}
        if selected in valid_ids:
            answers[str(question.id)] = selected
            request.session["quiz_answers"] = answers
        if "next" in request.POST:
            index = min(index + 1, total - 1)
        elif "previous" in request.POST:
            index = max(index - 1, 0)
        elif "finish" in request.POST:
            score = 0
            for item in questions:
                correct = next((a for a in item.reponses_level_one.all() if a.est_correcte), None)
                if correct and answers.get(str(item.id)) == str(correct.id):
                    score += 1
            LevelOneResult.objects.create(utilisateur=request.user.username, score=score)
            request.session["quiz_score"] = score
            request.session["quiz_total"] = total
            request.session.pop("quiz_answers", None)
            return redirect("quiz_result")
        return redirect(f"{request.path}?q={index}")
    if request.session.get("quiz_total") is not None and request.session.get("quiz_score") is not None:
        return redirect("quiz_result")
    return render(request, "quiz_question.html", {
        "question": questions[index],
        "current_index": index,
        "total_questions": total,
        "selected_answer": answers.get(str(questions[index].id)),
        "is_first_question": index == 0,
        "is_last_question": index == total - 1,
        "progress_percent": round((index + 1) / total * 100),
    })


@login_required
def quiz_result(request):
    score = request.session.get("quiz_score")
    total = request.session.get("quiz_total")
    if score is None or total is None:
        return redirect("level_one_quiz")
    return render(request, "quiz_result.html", {"score": score, "total_questions": total})


@login_required
def submit_level_two_quiz(request):
    questions = list(LevelTwoQuestion.objects.prefetch_related("reponses_level_two").order_by("numero"))
    if request.method == "POST":
        score = 0
        for question in questions:
            selected = (request.POST.get(f"q{question.id}") or "").strip()
            correct = next((a for a in question.reponses_level_two.all() if a.est_correcte), None)
            if correct and selected == str(correct.id):
                score += 1
        LevelTwoResult.objects.create(utilisateur=request.user.username, score=score)
        messages.success(request, f"Your score: {score}/{len(questions)}.")
        return redirect("level_two_quiz")
    return render(request, "level_two_quiz.html", {"questions": questions})


@login_required
def submit_level_three_quiz(request):
    questions = list(LevelThreeQuestion.objects.prefetch_related("reponses").order_by("numero"))
    if request.method == "POST":
        score = 0
        for question in questions:
            selected = (request.POST.get(f"q{question.id}") or "").strip()
            correct = next((a for a in question.reponses.all() if a.est_correcte), None)
            if correct and selected == str(correct.id):
                score += 1
        LevelThreeResult.objects.create(utilisateur=request.user.username, score=score)
        messages.success(request, f"Your score: {score}/{len(questions)}.")
        return redirect("level_three_quiz")
    return render(request, "level_three_quiz.html", {"questions": questions})


@login_required
def level_two_dashboard(request):
    return render(request, "level_two.html")


@login_required
def level_three_dashboard(request):
    return render(request, "level_three.html")


@login_required
def level_two_lesson(request):
    return render(request, "level_two_lesson.html")
