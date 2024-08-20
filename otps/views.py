from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.mail import send_mail
import pyotp
from django.contrib.auth.models import User
from django.conf import settings

# Define a secure secret key; this should be stored securely
SECRET_KEY = 'base32secret3232'

def send_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otp = pyotp.TOTP(SECRET_KEY, interval=300)  # OTP valid for 5 minutes
        otp_code = otp.now()

        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}.',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        request.session['otp_code'] = otp_code
        request.session['email'] = email
        return redirect('verify_otp')
    
    return render(request, 'send_otp.html')

def verify_otp_view(request):
    if request.method == 'POST':
        user_input_code = request.POST.get('otp_code')
        stored_otp_code = request.session.get('otp_code')
        email = request.session.get('email')

        otp = pyotp.TOTP(SECRET_KEY, interval=300)  # Same interval for verification

        # Debugging outputs
        print(f"Generated OTP: {stored_otp_code}")
        print(f"User Input OTP: {user_input_code}")

        if otp.verify(user_input_code) and stored_otp_code == user_input_code:
            try:
                # user = User.objects.get(email=email)
                # user.is_email_verified = True
                # user.save()
                return HttpResponse("Email verified successfully")
            except User.DoesNotExist:
                return HttpResponse("User not found")
        else:
            return HttpResponse("Invalid OTP")

    return render(request, 'verify_otp.html')
