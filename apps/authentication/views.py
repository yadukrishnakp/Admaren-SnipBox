import os
import sys
from typing import Any
from rest_framework import generics, status
from apps.authentication.schemas import LoginResponseSchema
from apps.authentication.serializers import LoginSerializer, LogoutSerializer, RefreshTokenSerializer
from apps.user.models import GeneratedAccessToken, Users
from snipbox_core.helpers.response import ResponseInfo
from snipbox_core.helpers.custom_messages import _account_tem_suspended, _invalid_credentials
from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from django.contrib import auth
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView

# User Login
class LoginApiView(generics.GenericAPIView):
    
    def __init__(self, **kwargs: Any):
        self.response_format = ResponseInfo().response
        super(LoginApiView, self).__init__(**kwargs)
        
    serializer_class = LoginSerializer
    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            
            if not serializer.is_valid():
                self.response_format['status']      = True
                self.response_format['errors']      = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            # Checking the Authentication
            user = auth.authenticate(
                username=serializer.validated_data.get("username", ""),
                password=serializer.validated_data.get("password", ""),
            )
            
            if user:
                if not user.is_active:
                    data = {'user': {}, 'token': '', 'refresh': ''}
                    self.response_format['status_code'] = status.HTTP_406_NOT_ACCEPTABLE
                    self.response_format['stauts']      = False
                    self.response_format['data']        = data
                    self.response_format['message']     = _account_tem_suspended
                    return Response(self.response_format, status=status.HTTP_200_OK)
                
                else:
                    # creating access and refresh tokens
                    serializer    = LoginResponseSchema(user, context={"request": request})
                    refresh       = RefreshToken.for_user(user)
                    token         = str(refresh.access_token)
                    data          = {'user': serializer.data, 'token':token, 'refresh': str(refresh)}
                    GeneratedAccessToken.objects.create(user=user, token=token)
                    
                    self.response_format['status_code'] = status.HTTP_200_OK
                    self.response_format['status']      = True
                    self.response_format['data']        = data
                    return Response(self.response_format, status=status.HTTP_200_OK)
            else:
                
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["message"] = _invalid_credentials
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_200_OK)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                
# Creating access token with use of refresh token
class RefreshTokenView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RefreshTokenSerializer

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(RefreshTokenView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            user = Users.objects.get(id=request.user.id)
            refresh = RefreshToken.for_user(user)
            data = {'token': str(
                refresh.access_token), 'refresh': str(refresh)}
            self.response_format['status_code'] = 200
            self.response_format["data"] = data
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# For log out
class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (IsAuthenticated,)

    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(LogoutAPIView, self).__init__(**kwargs)

    @swagger_auto_schema(tags=["Authorization"])
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            self.response_format['status'] = True
            self.response_format['status_code'] = status.HTTP_200_OK
            return Response(self.response_format, status=status.HTTP_200_OK)
        except Exception as e:
            self.response_format['status'] = False
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)