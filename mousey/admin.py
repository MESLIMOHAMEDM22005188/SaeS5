from django.contrib import admin
from .models import (
    QuestionLevelOne, ReponseLevelOne, ResultatLevelOne,
    QuestionLevelTwo, ReponseLevelTwo, ResultatLevelTwo,
    QuestionLevelThree, ResultatLevelThree, ReponseLevelThree
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


# --- Pour le Niveau 2 ---
# Étant donné que ReponseLevelTwo ne pointe pas vers QuestionLevelTwo,
# nous ne pouvons pas l'inclure en inline dans QuestionLevelTwo.
@admin.register(QuestionLevelTwo)
class QuestionLevelTwoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'texte')
    # Pas d'inlines ici, car ReponseLevelTwo n'est pas relié à QuestionLevelTwo

@admin.register(ResultatLevelTwo)
class ResultatLevelTwoAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'score', 'date')

# Enregistrement séparé de ReponseLevelTwo pour pouvoir les gérer individuellement
@admin.register(ReponseLevelTwo)
class ReponseLevelTwoAdmin(admin.ModelAdmin):
    list_display = ('texte', 'est_correcte', 'question')

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