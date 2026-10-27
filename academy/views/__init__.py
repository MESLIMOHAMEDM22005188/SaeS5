"""Compatibility exports for domain-specific view modules."""
from .accounts import login_view, register_view, send_verification_email, send_verification_sms, verify_email_code, verify_phone_code
from .games import browser_simulation, level_one_desktop, level_one_intro, level_two_game_four, level_two_game_one, level_two_game_three, level_two_game_two, password_game, phishing_warning, save_password_game_result
from .learning import level_one_quiz, level_three_dashboard, level_two_dashboard, level_two_lesson, quiz_result, submit_level_one_quiz, submit_level_three_quiz, submit_level_two_quiz
from .pages import dashboard

__all__ = [name for name in globals() if not name.startswith("_")]
