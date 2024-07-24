import os, sys 
from django.shortcuts import render
from drf_yasg import openapi
from rest_framework.response import Response
from apps.snippets_management.models import Snippet
from apps.snippets_management.schemas import GetSnippentDetailedViewSchema, GetSnippentsListSchema
from apps.snippets_management.serializers import CreateOrUpdateSnippetSerializer, UpdateSnippetserializer
from snipbox_core.helpers.helper import get_object_or_none
from snipbox_core.helpers.pagination import RestPagination
from snipbox_core.helpers.response import ResponseInfo
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,status
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from snipbox_core.helpers.custom_messages import _success,_record_not_found

# Create your views here.

class GetSnippetsCountAndDeatilsListApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetSnippetsCountAndDeatilsListApiView, self).__init__(**kwargs)
    
    serializer_class    = GetSnippentsListSchema
    permission_classes  = (IsAuthenticated,)
    pagination_class    = RestPagination
  
    @swagger_auto_schema(tags=["Snippets"], pagination_class=RestPagination)
    def get(self, request):
        
        try:
            queryset    = Snippet.objects.all().order_by('-id')
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



class CreateSnippetsApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(CreateSnippetsApiView, self).__init__(**kwargs)
        
    serializer_class = CreateOrUpdateSnippetSerializer
    permission_classes = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Snippets"])
    def post(self, request):
        try:

            serializer = self.serializer_class(data=request.data, context = {'request' : request})
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
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        


class UpdateSnippetsApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(UpdateSnippetsApiView, self).__init__(**kwargs)
    
    serializer_class          = UpdateSnippetserializer
    response_schema_class     = GetSnippentDetailedViewSchema
    permission_classes        = (IsAuthenticated,)
    
    @swagger_auto_schema(tags=["Snippets"])
    def put(self, request):
        try:

            snippet_instance = get_object_or_none(Snippet, pk=request.data.get('id'))
            
            if snippet_instance is None:
                self.response_format['status_code'] = status.HTTP_204_NO_CONTENT
                self.response_format["message"] = _record_not_found
                self.response_format["status"] = False
                return Response(self.response_format, status=status.HTTP_200_OK)

            serializer = self.serializer_class(snippet_instance,data=request.data, context = {'request' : request})
            
            if not serializer.is_valid():
                self.response_format['status_code'] = status.HTTP_400_BAD_REQUEST
                self.response_format["status"] = False
                self.response_format["errors"] = serializer.errors
                return Response(self.response_format, status=status.HTTP_400_BAD_REQUEST)
            
            snippet_instance = serializer.save()

            self.response_format['status_code'] = status.HTTP_201_CREATED
            self.response_format["message"] = _success
            self.response_format["data"] = self.response_schema_class(snippet_instance, context={'request': request}).data
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = str(e)
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  