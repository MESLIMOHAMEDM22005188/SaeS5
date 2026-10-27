from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login as auth_login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.utils import timezone
from academy.forms import RegistrationForm
from academy.models import EmailVerification, PhoneVerification

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=(request.POST.get('username') or '').strip(), password=request.POST.get('password') or '')
        if user is None:
            messages.error(request, 'Invalid username or password.')
        elif not user.is_active:
            messages.error(request, 'Your account is not active. Complete email verification first.')
        else:
            auth_login(request, user)
            messages.success(request, 'You are now signed in.')
            return redirect('home')
    return render(request, 'registration/login.html')

def send_verification_email(user):
    verification, _ = EmailVerification.objects.get_or_create(user=user, defaults={'email': user.email})
    verification.email = user.email
    verification.generate_code()
    send_mail('Verify your email address', f'Your verification code is: {verification.verification_code}', settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)

def send_verification_sms(phone_number, code):
    if not all((settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN, settings.TWILIO_PHONE_NUMBER)):
        return False
    try:
        from twilio.rest import Client
        Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN).messages.create(body=f'Your verification code is: {code}', from_=settings.TWILIO_PHONE_NUMBER, to=phone_number)
        return True
    except Exception:
        return False

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            phone = PhoneVerification.objects.create(user=user, phone_number=form.cleaned_data['phone_number'])
            email, _ = EmailVerification.objects.get_or_create(user=user, defaults={'email': user.email})
            phone.generate_code()
            email.email = user.email
            email.save(update_fields=['email', 'updated_at'])
            sms_sent = send_verification_sms(phone.phone_number, phone.verification_code)
            try:
                send_verification_email(user)
            except Exception:
                messages.error(request, 'Email delivery failed. Check the SMTP configuration.')
                return render(request, 'registration.html', {'form': form}, status=503)
            if not sms_sent:
                messages.warning(request, 'SMS delivery is not configured. The account will remain inactive until phone verification.')
            messages.success(request, 'Check your phone and email to activate your account.')
            return redirect('verify_phone', identifier=user.username)
        messages.error(request, 'Please correct the errors in the registration form.')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def verify_phone_code(request, identifier):
    user = get_user_model().objects.filter(username=identifier).first()
    if user is None:
        messages.error(request, 'Account not found.')
        return redirect('register')
    if request.method == 'POST':
        code = (request.POST.get('code') or '').strip()
        verification = PhoneVerification.objects.filter(user=user).first()
        if verification and not verification.is_verified and verification.verification_code and verification.verification_code == code and verification.code_expiration and verification.code_expiration > timezone.now():
            verification.is_verified = True
            verification.verification_code = None
            verification.save(update_fields=['is_verified', 'verification_code', 'updated_at'])
            request.session['pending_verification_user_id'] = user.pk
            messages.success(request, 'Phone number verified.')
            return redirect('verify_email')
        messages.error(request, 'The verification code is invalid or has expired.')
    return render(request, 'verify.html', {'identifier': identifier})

def verify_email_code(request):
    pending_id = request.session.get('pending_verification_user_id')
    if not pending_id:
        messages.error(request, 'Verify your phone number before verifying your email.')
        return redirect('register')
    if request.method != 'POST':
        return render(request, 'verify_email.html')
    code = (request.POST.get('code') or '').strip()
    verification = EmailVerification.objects.filter(user_id=pending_id, verification_code=code, is_verified=False).select_related('user').first()
    if not verification or not verification.is_code_valid():
        messages.error(request, 'The verification code is invalid or has expired.')
        return render(request, 'verify_email.html', status=400)
    verification.is_verified = True
    verification.verification_code = None
    verification.save(update_fields=['is_verified', 'verification_code', 'updated_at'])
    verification.user.is_active = True
    verification.user.save(update_fields=['is_active'])
    request.session.pop('pending_verification_user_id', None)
    messages.success(request, 'Email verified. You can now sign in.')
    return redirect('login')
