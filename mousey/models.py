from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta


class EmailGame(models.Model):
    id = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.subject


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
        """
        Génère un code de vérification à 6 chiffres et définit la date d'expiration.
        """
        import random
        self.verification_code = str(random.randint(100000, 999999))
        self.code_expiration = now() + timedelta(minutes=10)
        self.save()

    def is_code_valid(self):
        """
        Vérifie si le code est encore valide.
        """
        return self.code_expiration and now() <= self.code_expiration

    def __str__(self):
        return f"{self.user.username} - {self.email} - Verified: {self.is_verified}"