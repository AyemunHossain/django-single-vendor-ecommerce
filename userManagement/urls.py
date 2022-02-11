
from django.conf.urls import include
from django.urls import path
from django.conf.urls import url
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .apiView import *

app_name = 'usermanagement'

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/login/', LoginAPIView.as_view(), name='login_user'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/blacklist/', BlacklistTokenAdding.as_view(), name='blacklist'),
    path('api/register/', RegisterUser.as_view(), name="register_new_user"),
    path('api/request-verify-email/', EmailVerifyRequest.as_view(), name="request_verify_new_user"),
    path('api/verify-email/', VerifyEmail.as_view(), name="verify_new_user"),
    path('api/request-reset-password/', RequestPasswordResetEmail.as_view(), name="request_reset_your_password"),
    path('api/validate-reset-token/', ValidateResetToken.as_view(), name="validate_reset_token"),
    path('api/reset-password/', ResetPassword.as_view(), name="reset_password"),
    
    
    # path('api/user-status/', GetUserStatusAndDetails.as_view(),
    #      name="is_authenticated_user"),
]
