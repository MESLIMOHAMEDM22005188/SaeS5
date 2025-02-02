from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

class Forteresse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Relation avec l'utilisateur
    password = models.CharField(max_length=255)  # Mot de passe créé
    strength = models.CharField(max_length=50)  # Force du mot de passe (faible, moyen, fort)
    porte_status = models.BooleanField(default=False)  # État de la porte (fermée ou ouverte)
    tour_droite_status = models.BooleanField(default=False)  # État de la tour droite
    tour_gauche_status = models.BooleanField(default=False)  # État de la tour gauche
    created_at = models.DateTimeField(auto_now_add=True)  # Date de création

    def __str__(self):
        return f"Forteresse de {self.user.username} - {self.strength}"


class EmailGame(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.subject


class QuestionLevelOne(models.Model):
    texte = models.TextField()
    numero = models.IntegerField()
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)

    def __str__(self):
        return f"Question {self.numero}: {self.texte}"


class QuestionLevelTwo(models.Model):
    texte = models.TextField()
    numero = models.IntegerField()
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)

    def __str__(self):
        return f"Question {self.numero}: {self.texte}"


class QuestionLevelThree(models.Model):
    texte = models.TextField()
    numero = models.IntegerField()
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)

    def __str__(self):
        return f"Question {self.numero}: {self.texte}"


class ReponseLevelOne(models.Model):
    question = models.ForeignKey(
        QuestionLevelOne,
        on_delete=models.CASCADE,
        related_name='reponses_level_one'
    )
    texte = models.CharField(max_length=200)
    est_correcte = models.BooleanField(default=False)

    def __str__(self):
        return f"Réponse: {self.texte} (Correcte: {self.est_correcte})"


class ReponseLevelTwo(models.Model):
    # Option A : modification pour que ReponseLevelTwo référence QuestionLevelTwo
    question = models.ForeignKey(
        QuestionLevelTwo,
        on_delete=models.CASCADE,
        related_name='reponses_level_two'
    )
    texte = models.CharField(max_length=200)
    est_correcte = models.BooleanField(default=False)

    def __str__(self):
        return f"Réponse: {self.texte} (Correcte: {self.est_correcte})"


class ReponseLevelThree(models.Model):
    question = models.ForeignKey(
        QuestionLevelThree,
        on_delete=models.CASCADE,
        related_name='reponses'  # Pour simplifier le template
    )
    texte = models.CharField(max_length=200)
    est_correcte = models.BooleanField(default=False)

    def __str__(self):
        return f"Réponse: {self.texte} (Correcte: {self.est_correcte})"


class ResultatLevelOne(models.Model):
    utilisateur = models.CharField(max_length=100)
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur} - {self.score} points"


class ResultatLevelTwo(models.Model):
    utilisateur = models.CharField(max_length=100)
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur} - {self.score} points"


class ResultatLevelThree(models.Model):
    utilisateur = models.CharField(max_length=100)
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur} - {self.score} points"


class PhoneVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='phone_verification')
    phone_number = models.CharField(max_length=15, unique=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code_expiration = models.DateTimeField(null=True, blank=True)

    def generate_code(self):
        import random
        self.verification_code = str(random.randint(100000, 999999))
        self.code_expiration = now() + timedelta(minutes=10)
        self.save()

    def __str__(self):
        return f"{self.user.username} - {self.phone_number} - Verified: {self.is_verified}"


class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='email_verification')
    email = models.EmailField(unique=True)
    verification_code = models.CharField(max_length=6, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    code_expiration = models.DateTimeField(null=True, blank=True)

    def generate_code(self):
        import random
        self.verification_code = str(random.randint(100000, 999999))
        self.code_expiration = now() + timedelta(minutes=10)
        self.save()

    def is_code_valid(self):
        return self.code_expiration and now() <= self.code_expiration

    def __str__(self):
        return f"{self.user.username} - {self.email} - Verified: {self.is_verified}"
