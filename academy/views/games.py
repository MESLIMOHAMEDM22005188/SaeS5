"""Cybersecurity simulations and mini-game pages."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from academy.models import FortressGame


@login_required
def phishing_warning(request):
    return render(request, "screen_warning.html")


@login_required
def level_one_intro(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        # This is an awareness simulation, never a real authentication endpoint.
        if username and password:
            messages.info(request, "Simulation: never enter real credentials on an untrusted page.")
            return redirect("phishing_warning")
        messages.error(request, "Enter both fields to run the simulation.")
    return render(request, "level_one.html")


@login_required
def level_one_desktop(request):
    return render(request, "level_one_desktop.html")


@login_required
def level_two_game_one(request):
    return render(request, "level_two_game_one.html")


@login_required
def level_two_game_two(request):
    return render(request, "level_two_game_two.html")


@login_required
def level_two_game_three(request):
    return render(request, "level_two_game_three.html")


@login_required
def level_two_game_four(request):
    return render(request, "level_two_game_four.html")


@login_required
def password_game(request):
    return render(request, "password_game.html")


@login_required
def browser_simulation(request):
    return render(request, "browser_simulation.html")


@login_required
def save_password_game_result(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed."}, status=405)
    submitted_password = (request.POST.get("password") or "").strip()
    strength = (request.POST.get("strength") or "weak").strip().lower()
    if not submitted_password:
        return JsonResponse({"error": "A password is required."}, status=400)
    if strength not in {"weak", "medium", "strong"}:
        return JsonResponse({"error": "Invalid password strength."}, status=400)
    # Persist the result category, never the entered secret itself.
    FortressGame.objects.create(user=request.user, password="", strength=strength)
    return JsonResponse({"message": "Game progress saved."}, status=201)
