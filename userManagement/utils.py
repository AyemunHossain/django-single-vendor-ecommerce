import concurrent.futures
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.core.mail import send_mail
from django.conf import settings
from userManagement.models import UserAccount as User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import smart_bytes, smart_str
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def try_email_send(data):
    subject = data['email_subject']
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [data['to_email'], ]
    try:
        val = send_mail(subject, message="", html_message=data['email_body'],
                        from_email=email_from, recipient_list=recipient_list)
    except Exception as e:
        val = e
    return val

class EmailVarification:
    @staticmethod
    def send_email(data):
        token = get_tokens_for_user(data['user'])
        absurl = 'http://'+data['current_site']+data['relativeLink']+"?token="+token
        email_body = render_to_string('acc_active_email.html', {
            'user': data['user'].username,
            'absurl': absurl,
        })
        data['email_body'] = email_body
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(try_email_send, data)
            return_value = future.result()
            if return_value == 1:
                return {"status": 200, "message" : "Varification details sent to your email, please check"}
            else:
                return {"status": 400, "message": return_value}


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()


class PasswordChangeRequest:
    @staticmethod
    def send_email(data): 
        try:
            user = User.objects.get(email=data['to_email'])
            
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            
            absurl = 'http://'+data['current_site'] + \
                data['relativeLink']+"?uidb64="+uidb64+"&token=" + \
                account_activation_token.make_token(user)
                
            email_body = render_to_string('password_reset_email.html', {
                'absurl': absurl,
            })
            data['email_body'] = email_body
            
            print(f"-----------------------{absurl}-------------------------------")
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(try_email_send, data)
                return_value = future.result()
                if return_value == 1:
                    return {"status": 200, "message": "Password reset details sent to your email, please check"}
                else:
                    return {"status": 400, "message": return_value}
        except Exception as e:
            return {"status": 400, "message": e}

    @staticmethod
    def check_reset_token(data):
        try:
            id = smart_str(urlsafe_base64_decode(data['uidb64']))
            user = User.objects.get(id=id)
            ret_val = account_activation_token.check_token(user, data['token'])
            return account_activation_token.check_token(user,data['token'])
        
        except Exception as e:
            return e