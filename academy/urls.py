from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

urlpatterns = [
    path("", views.register_view, name="register"),
    path("home/", views.dashboard, name="home"),
    path("verify-phone/<str:identifier>/", views.verify_phone_code, name="verify_phone"),
    path("verify-email/", views.verify_email_code, name="verify_email"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("level-one/", views.level_one_intro, name="level_one"),
    path("level-one/desktop/", views.level_one_desktop, name="level_one_desktop"),
    path("level-one/browser/", views.browser_simulation, name="browser_simulation"),
    path("level-one/quiz/", views.level_one_quiz, name="level_one_quiz"),
    path("level-one/quiz/submit/", views.submit_level_one_quiz, name="submit_level_one_quiz"),
    path("level-one/quiz/result/", views.quiz_result, name="quiz_result"),
    path("level-two/", views.level_two_dashboard, name="level_two"),
    path("level-two/game-one/", views.level_two_game_one, name="level_two_game_one"),
    path("level-two/game-two/", views.level_two_game_two, name="level_two_game_two"),
    path("level-two/game-three/", views.level_two_game_three, name="level_two_game_three"),
    path("level-two/game-four/", views.level_two_game_four, name="level_two_game_four"),
    path("level-two/password-game/", views.password_game, name="password_game"),
    path("level-two/lesson/", views.level_two_lesson, name="level_two_lesson"),
    path("level-two/quiz/", views.submit_level_two_quiz, name="level_two_quiz"),
    path("level-three/", views.level_three_dashboard, name="level_three"),
    path("level-three/quiz/", views.submit_level_three_quiz, name="level_three_quiz"),
    path("phishing-warning/", views.phishing_warning, name="phishing_warning"),
    path("save-password/", views.save_password_game_result, name="save_password_game_result"),
]
