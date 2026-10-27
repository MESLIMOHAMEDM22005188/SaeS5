from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import EmailVerification, PhoneVerification


class RegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        required=True,
        label="Phone number",
        widget=forms.TextInput(attrs={"placeholder": "Example: +33612345678"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "phone_number", "password1", "password2"]

    def clean_email(self):
        email = (self.cleaned_data.get("email") or "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        if EmailVerification.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("This email address is already linked to an account.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get("phone_number")
        if PhoneVerification.objects.filter(phone_number=phone_number).exists():
            raise forms.ValidationError("This phone number is already in use.")
        return phone_number
