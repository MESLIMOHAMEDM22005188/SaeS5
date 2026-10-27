from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import EmailVerification, PhoneVerification


class VerificationCodeModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="learner",
            email="learner@example.test",
            password="TestPassword!42",
        )

    def test_phone_code_is_six_digits_and_expires(self):
        verification = PhoneVerification.objects.create(
            user=self.user,
            phone_number="+33600000000",
        )
        verification.generate_code()

        self.assertRegex(verification.verification_code, r"^\d{6}$")
        self.assertGreater(verification.code_expiration, timezone.now())
        self.assertLessEqual(
            verification.code_expiration,
            timezone.now() + timedelta(minutes=11),
        )

    def test_email_code_is_six_digits_and_expires(self):
        verification = EmailVerification.objects.create(
            user=self.user,
            email=self.user.email,
        )
        verification.generate_code()

        self.assertRegex(verification.verification_code, r"^\d{6}$")
        self.assertTrue(verification.is_code_valid())

    def test_email_verification_requires_pending_user_in_session(self):
        verification = EmailVerification.objects.create(
            user=self.user,
            email=self.user.email,
            verification_code="123456",
            code_expiration=timezone.now() + timedelta(minutes=10),
        )

        response = self.client.post(
            reverse("verify_email"),
            {"code": "123456"},
        )

        self.assertRedirects(response, reverse("register"))
        verification.refresh_from_db()
        self.assertFalse(verification.is_verified)

    def test_email_code_activates_only_the_pending_account(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])
        EmailVerification.objects.create(
            user=self.user,
            email=self.user.email,
            verification_code="123456",
            code_expiration=timezone.now() + timedelta(minutes=10),
        )
        session = self.client.session
        session["pending_verification_user_id"] = self.user.pk
        session.save()

        response = self.client.post(
            reverse("verify_email"),
            {"code": "123456"},
        )

        self.assertRedirects(response, reverse("login"))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertIsNone(
            EmailVerification.objects.get(user=self.user).verification_code
        )

    def test_expired_email_code_is_rejected(self):
        verification = EmailVerification.objects.create(
            user=self.user,
            email=self.user.email,
            verification_code="123456",
            code_expiration=timezone.now() - timedelta(minutes=1),
        )
        session = self.client.session
        session["pending_verification_user_id"] = self.user.pk
        session.save()

        response = self.client.post(
            reverse("verify_email"),
            {"code": "123456"},
        )

        self.assertEqual(response.status_code, 400)
        verification.refresh_from_db()
        self.assertFalse(verification.is_verified)
