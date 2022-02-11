from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from .serializers import *
from django.shortcuts import get_object_or_404
from .utils import EmailVarification, PasswordChangeRequest, get_tokens_for_user
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.urls import reverse
from django.shortcuts import redirect, reverse as Reverse
import jwt
from django.conf import settings
from .models import UserAccount as User
from rest_framework import generics

class BlacklistTokenAdding(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, format='json'):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RegisterUser(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterUserSerializer
    def post(self,request,format="json"):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            try:
                newUser = serializer.save()
                if newUser:
                    response = serializer.data
                    return Response(response, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
        return Response(serializer.errors or None, status=status.HTTP_400_BAD_REQUEST)
    
    
class EmailVerifyRequest(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication,]
    def get(self,request,format="json"):
        try:
            if(request.user.is_verified is False):
                data = {'to_email': request.user.email, 'email_subject': 'Verify your email',
                        'user': request.user, 'relativeLink': reverse('usermanagement:verify_new_user'), 'current_site': get_current_site(request).domain}
                response = EmailVarification.send_email(data)
                
                return Response({"status": response["status"],"message":response["message"]}, status=status.HTTP_200_OK)
            else:
                return Response({"email":"Already Varified"},status=status.HTTP_200_OK)
            
        except Exception as e:
            print(f"------------------>>>>>{e}<<<<----------------------")
            return Response(status=status.HTTP_400_BAD_REQUEST)


class VerifyEmail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    
    def get(self, request, format="json"):
        token = request.GET.get('token')
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            
            user = User.objects.get(id=payload['user_id'])
            print(
                f"-------------------------->>>>>{request.user.id} <<<<----------------")
            if request.user.id == user.id:
                if user.is_verified == False:
                    user.is_verified = True
                    user.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response({"email": "Already Varified"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'This token is forbidden'}, status=status.HTTP_400_BAD_REQUEST)
            
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': 'Unknown Error Occured, try to get another varification message.'}, status=status.HTTP_400_BAD_REQUEST)



class RequestPasswordResetEmail(APIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, format="json"):
        try:
            serializer = self.serializer_class(data=request.data)
            email = request.data.get('email', '')
            if User.objects.filter(email=email).exists():
                data = {'to_email': email, 'email_subject': 'Reset your password', 'relativeLink': reverse('usermanagement:validate_reset_token'),
                        'current_site': get_current_site(request).domain}
                response = PasswordChangeRequest.send_email(data)
                
                return Response({"status": response["status"], "message": response["message"]}, status=status.HTTP_200_OK)
            else:
                return Response({"response": "No input email"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error":e},status=status.HTTP_400_BAD_REQUEST)
   

class ValidateResetToken(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request, format="json"):
        
        if(request.GET['token'] != None and request.GET['uidb64'] != None):
            data = {}
            data['uidb64'] = request.GET['uidb64']
            data['token'] = request.GET['token']
            ret_val = PasswordChangeRequest.check_reset_token(data)
            if ret_val==True:
                return Response({"redirect": True}, status=status.HTTP_200_OK)
            
            return Response({"error": "Error with token or uidb64"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "No token found"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPassword(APIView):
    """
    Future: You should dismiss all other token of user so that the security issue with that will be solved
    """
    serializer_class = SetNewPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, format="json"):
        serializer = self.serializer_class(data={'token': request.GET['token'], "uidb64": request.GET['uidb64'],'password': request.data.get('password')})
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


















# class GetUserStatusAndDetails(APIView):
#     permission_classes = [permissions.AllowAny]

#     def get(self, request):
#         auth = request.user.is_authenticated
#         if(auth):

#             try:
#                 avatar = get_object_or_404(UserProfile, user__id=request.user.id).avatar
#             except:
#                 avatar = None

#             try:
#                 admin = request.user.is_superuser
#             except:
#                 admin = False

#             try:
#                 content = {
#                     'auth': auth,
#                     'admin': admin,
#                     'username': request.user.username,
#                     'email': request.user.email,
#                     'avatar': avatar
#                 }
#                 serializer = UserDetailsForNav(content)
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             except Exception as E:
#                 print(f'-----------------------{E}')

#                 return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
#         else:
#             print(f"----------------Unauthenticated ......................")
#             return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
