from django.forms.widgets import FileInput
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

class MultiFileInputWidget(FileInput):
    allows_multiple_files = True

    def __init__(self, attributes=None):
        super().__init__(attributes)
        if attributes is None:
            attributes = {}
        attributes.update({'multiple': True})
        self.attrs = attributes

    def value_from_datadict(self, data, files, field_name):
        if hasattr(files, 'getlist'):
            return files.getlist(field_name)
        return files.get(field_name)

def create_random_otp(length=6):
    digit_set = string.digits
    otp_code = ''.join(random.choices(digit_set, k=length))
    return otp_code

def dispatch_otp_via_email(account_user):
    otp_code = create_random_otp()
    account_user.profile.otp_code = otp_code
    account_user.profile.save()

    email_subject = 'Your One-Time Password (OTP)'
    email_body = f'Your One-Time Password is: {otp_code}'
    sender_email = settings.EMAIL_HOST_USER
    recipients = [account_user.email]
    
    send_mail(email_subject, email_body, sender_email, recipients)

@api_view(['POST'])
def validate_otp(request):
    user_email = request.data.get('email')
    input_otp = request.data.get('otp')

    try:
        account_user = User.objects.get(email=user_email)
        if account_user.profile.otp_code == input_otp:
            account_user.profile.otp_code = ''
            account_user.profile.save()
            return Response({'message': 'OTP successfully validated'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Provided OTP is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'message': 'No account associated with this email'}, status=status.HTTP_404_NOT_FOUND)