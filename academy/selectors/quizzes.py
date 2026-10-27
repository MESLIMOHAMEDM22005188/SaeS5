"""Reusable read-side queries for quiz content."""
from academy.models import LevelOneQuestion, LevelThreeQuestion, LevelTwoQuestion


def get_level_one_questions():
    return LevelOneQuestion.objects.prefetch_related("reponses_level_one").order_by("numero")


def get_level_two_questions():
    return LevelTwoQuestion.objects.prefetch_related("reponses_level_two").order_by("numero")


def get_level_three_questions():
    return LevelThreeQuestion.objects.prefetch_related("reponses").order_by("numero")
