from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now, timedelta

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