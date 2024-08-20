import pyotp
from django.core.mail import send_mail
from django.contrib.auth.models import User

def handle_otp_verification(user_email, user_input_code=None):
    # Define a secure secret key; this should be stored securely
    secret_key = 'base32secret3232'

    otp = pyotp.TOTP(secret_key)
    
    if user_input_code:
        # User is trying to verify their OTP
        if otp.verify(user_input_code):
            try:
                user = User.objects.get(email=user_email)
                user.is_email_verified = True
                user.save()
                return "Email verified successfully"
            except User.DoesNotExist:
                return "User not found"
        else:
            return "Invalid OTP"
    else:
        # Generate and send OTP
        otp_code = otp.now()
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp_code}.',
            'from@example.com',
            [user_email],
            fail_silently=False,
        )
        return "OTP sent to email"
