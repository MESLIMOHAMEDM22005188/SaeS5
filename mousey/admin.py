from django.contrib import admin
from .models import (
    QuestionLevelOne, ReponseLevelOne, ResultatLevelOne,
    QuestionLevelTwo, ReponseLevelTwo, ResultatLevelTwo,
    QuestionLevelThree, ReponseLevelThree, ResultatLevelThree
)

# --- Inlines pour le Niveau 1 (questions avec leurs réponses) ---
class ReponseLevelOneInline(admin.TabularInline):
    model = ReponseLevelOne
    extra = 1

@admin.register(QuestionLevelOne)
class QuestionLevelOneAdmin(admin.ModelAdmin):
    list_display = ('numero', 'texte')
    inlines = [ReponseLevelOneInline]

@admin.register(ResultatLevelOne)
class ResultatLevelOneAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'score', 'date')

@admin.register(ReponseLevelOne)
class ReponseLevelOneAdmin(admin.ModelAdmin):
    list_display = ('texte', 'est_correcte', 'question')


# --- Inlines pour le Niveau 2 ---
# Vérifiez que dans le modèle, ReponseLevelTwo référence bien QuestionLevelTwo via la clé étrangère.
class ReponseLevelTwoInline(admin.TabularInline):
    model = ReponseLevelTwo
    extra = 1

@admin.register(QuestionLevelTwo)
class QuestionLevelTwoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'texte')
    inlines = [ReponseLevelTwoInline]

@admin.register(ResultatLevelTwo)
class ResultatLevelTwoAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'score', 'date')

@admin.register(ReponseLevelTwo)
class ReponseLevelTwoAdmin(admin.ModelAdmin):
    list_display = ('texte', 'est_correcte', 'question')


# --- Inlines pour le Niveau 3 ---
class ReponseLevelThreeInline(admin.TabularInline):
    model = ReponseLevelThree
    extra = 1

@admin.register(QuestionLevelThree)
class QuestionLevelThreeAdmin(admin.ModelAdmin):
    list_display = ('numero', 'texte')
    inlines = [ReponseLevelThreeInline]

@admin.register(ReponseLevelThree)
class ReponseLevelThreeAdmin(admin.ModelAdmin):
    list_display = ('texte', 'est_correcte', 'question')

@admin.register(ResultatLevelThree)
class ResultatLevelThreeAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'score', 'date')
