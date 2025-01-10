# admin.py
from django.contrib import admin
from .models import QuestionLevelOne, ReponseLevelOne, ResultatLevelOne


class ReponseInline(admin.TabularInline):
    model = ReponseLevelOne
    extra = 1


@admin.register(QuestionLevelOne)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('numero', 'texte')
    inlines = [ReponseInline]


@admin.register(ResultatLevelOne)
class ResultatAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'score', 'date')
