import sys,os
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from apps.user.models import  Users
from apps.user.schemas import GetUsersDetailApiSerializers, GetUsersListApiSerializers
from apps.user.serializers import  CreateOrUpdateUserSerializer
from snipbox_core.helpers.helper import get_object_or_none
from snipbox_core.helpers.pagination import RestPagination
from snipbox_core.helpers.response import ResponseInfo
from snipbox_core.helpers.custom_messages import _success,_record_not_found
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from drf_yasg import openapi


# User registration and updation of detailes are takesplace here.
class CreateOrUpdateUserApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateOrUpdateUserApiView, self).__init__(**kwargs)
        
    serializer_class = CreateOrUpdateUserSerializer
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Users"])
    def post(self, request):
        try:
            user_instance = get_object_or_none(Users,pk=request.data.get('user',None))
           
            serializer = self.serializer_class(user_instance, data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            
            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Return User deatils as list and also implemented search with username and email.
class GetUsersListApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetUsersListApiView, self).__init__(**kwargs)
    
    serializer_class    = GetUsersListApiSerializers
    permission_classes  = [IsAuthenticated]
    pagination_class    = RestPagination
  
    search        = openapi.Parameter('search', openapi.IN_QUERY, type=openapi.TYPE_STRING,description="The search value User name or Email", required=False)
  
    @swagger_auto_schema(tags=["Users"], manual_parameters=[search], pagination_class=RestPagination)
    def get(self, request):
        
        try:
            search_value    = request.GET.get('search', None)

            filter_set = Q()
            if search_value not in ['',None]:
                filter_set = Q(username=search_value) | Q(email=search_value)
     
            queryset    = Users.objects.filter(filter_set).order_by('-id')
            page        = self.paginate_queryset(queryset)
            serializer  = self.serializer_class(page, many=True,context={'request':request})
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 


# Return detailed view of user details with the use of id.
class GetUserDetailApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetUserDetailApiView, self).__init__(**kwargs)

    serializer_class = GetUsersDetailApiSerializers
    permission_classes  = (IsAuthenticated,)

    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING,required=True, description="Enter id")

    @swagger_auto_schema(tags=["Users"], manual_parameters=[id])
    def get(self, request):

        try:
            user_instance = get_object_or_none(Users, pk=request.GET.get('id', None))

            if user_instance is None:
                self.response_format['status_code'] = status.HTTP_204_NO_CONTENT
                self.response_format["message"] = _record_not_found
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_200_OK)

            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["data"] = self.serializer_class(user_instance, context={'request': request}).data
            self.response_format["message"] = _success
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)

        except Exception as e:

            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)