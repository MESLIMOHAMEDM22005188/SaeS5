from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Forteresse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Account associated with this game state
    password = models.CharField(max_length=255)  # Legacy field; submitted passwords are never stored
    strength = models.CharField(max_length=50)  # Password-strength category
    porte_status = models.BooleanField(default=False)  # Door state
    tour_droite_status = models.BooleanField(default=False)  # Right tower state
    tour_gauche_status = models.BooleanField(default=False)  # Left tower state
    created_at = models.DateTimeField(auto_now_add=True)  # Creation timestamp

    def __str__(self):
        return f"Fortress game for {self.user.username} - {self.strength}"


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

    @property
    def text(self):
        return self.texte

    @property
    def number(self):
        return self.numero

    @property
    def answers(self):
        cached_answers = getattr(self, "_english_answers", None)
        return cached_answers if cached_answers is not None else self.reponses_level_one.all()

    def __str__(self):
        return f"Question {self.numero}: {self.texte}"


class QuestionLevelTwo(models.Model):
    texte = models.TextField()
    numero = models.IntegerField()
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)

    @property
    def text(self):
        return self.texte

    @property
    def number(self):
        return self.numero

    @property
    def answers(self):
        cached_answers = getattr(self, "_english_answers", None)
        return cached_answers if cached_answers is not None else self.reponses_level_two.all()

    def __str__(self):
        return f"Question {self.numero}: {self.texte}"


class QuestionLevelThree(models.Model):
    texte = models.TextField()
    numero = models.IntegerField()
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)

    @property
    def text(self):
        return self.texte

    @property
    def number(self):
        return self.numero

    @property
    def answers(self):
        cached_answers = getattr(self, "_english_answers", None)
        return cached_answers if cached_answers is not None else self.reponses.all()

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

    @property
    def text(self):
        return self.texte

    @property
    def is_correct(self):
        return self.est_correcte

    def __str__(self):
        return f"Answer: {self.texte} (Correct: {self.est_correcte})"


class ReponseLevelTwo(models.Model):
    question = models.ForeignKey(
        QuestionLevelTwo,
        on_delete=models.CASCADE,
        related_name='reponses_level_two'
    )
    texte = models.CharField(max_length=200)
    est_correcte = models.BooleanField(default=False)

    @property
    def text(self):
        return self.texte

    @property
    def is_correct(self):
        return self.est_correcte

    def __str__(self):
        return f"Answer: {self.texte} (Correct: {self.est_correcte})"

class ReponseLevelThree(models.Model):
    question = models.ForeignKey(
        QuestionLevelThree,
        on_delete=models.CASCADE,
        related_name='reponses'
    )
    texte = models.CharField(max_length=200)
    est_correcte = models.BooleanField(default=False)

    @property
    def text(self):
        return self.texte

    @property
    def is_correct(self):
        return self.est_correcte

    def __str__(self):
        return f"Answer: {self.texte} (Correct: {self.est_correcte})"


class ResultatLevelOne(models.Model):
    utilisateur = models.CharField(max_length=100)
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    @classmethod
    def record_score(cls, username, score):
        return cls.objects.create(utilisateur=username, score=score)

    def __str__(self):
        return f"{self.utilisateur} - {self.score} points"


class ResultatLevelTwo(models.Model):
    utilisateur = models.CharField(max_length=100)
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    @classmethod
    def record_score(cls, username, score):
        return cls.objects.create(utilisateur=username, score=score)

    def __str__(self):
        return f"{self.utilisateur} - {self.score} points"


class ResultatLevelThree(models.Model):
    utilisateur = models.CharField(max_length=100)
    score = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    @classmethod
    def record_score(cls, username, score):
        return cls.objects.create(utilisateur=username, score=score)

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
        import secrets
        self.verification_code = f"{secrets.randbelow(900000) + 100000}"
        self.code_expiration = timezone.now() + timedelta(minutes=10)
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
        import secrets
        self.verification_code = str(secrets.randbelow(900000) + 100000)
        self.code_expiration = timezone.now() + timedelta(minutes=10)
        self.save()

    def is_code_valid(self):
        return bool(self.code_expiration and timezone.now() <= self.code_expiration)

    def __str__(self):
        return f"{self.user.username} - {self.email} - Verified: {self.is_verified}"


# English aliases keep application code readable without changing legacy database models.
FortressGame = Forteresse
LevelOneQuestion = QuestionLevelOne
LevelTwoQuestion = QuestionLevelTwo
LevelThreeQuestion = QuestionLevelThree
LevelOneAnswer = ReponseLevelOne
LevelTwoAnswer = ReponseLevelTwo
LevelThreeAnswer = ReponseLevelThree
LevelOneResult = ResultatLevelOne
LevelTwoResult = ResultatLevelTwo
LevelThreeResult = ResultatLevelThree
