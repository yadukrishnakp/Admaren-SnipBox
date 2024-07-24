import os, sys 
from drf_yasg import openapi
from rest_framework.response import Response
from apps.snippets_management.models import Snippet, Tag
from apps.snippets_management.schemas import GetSnippentDetailedViewSchema, GetSnippentsListSchema, GetSnippetsDetailsCurrentUserApiSchema, GetTagListSchema
from apps.snippets_management.serializers import CreateOrUpdateSnippetSerializer, DeleteSnippetSerializer, UpdateSnippetserializer
from snipbox_core.helpers.helper import get_object_or_none
from snipbox_core.helpers.pagination import RestPagination
from snipbox_core.helpers.response import ResponseInfo
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,status
from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from snipbox_core.helpers.custom_messages import _success,_record_not_found

# Create your views here.


# Return All the snippets and its count with pagination
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


# Create the snippets with unique tag name
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
        

# Update the snippets with unique tag name
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


# Return the snippets, also check the current user, return snippets if the current both current user and created user are same
class GetSnippetsDeatilsCurrentUserApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetSnippetsDeatilsCurrentUserApiView, self).__init__(**kwargs)
        
    serializer_class = GetSnippetsDetailsCurrentUserApiSchema
    permission_classes = (IsAuthenticated,)

    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description="Enter Snippet id")
    
    @swagger_auto_schema(tags=["Snippets"], manual_parameters=[id])
    def get(self, request):
        
        try:
            instance_id    = request.GET.get('id', None)

            filter_set = Q()
            if instance_id not in ['',None]:
                filter_set = Q(id=instance_id) & Q(created_by_id=request.user.id)

            queryset    = Snippet.objects.filter(filter_set)
            serializer =  self.serializer_class(queryset, many=True, context={"request": request})
            self.response_format['status_code'] = status.HTTP_200_OK
            self.response_format["data"] = serializer.data 
            self.response_format["status"] = True
            return Response(self.response_format, status=status.HTTP_200_OK)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        

# Delete the snippets, can delete individual and multiple data.
class DeleteSnippetsApiView(generics.DestroyAPIView): 
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(DeleteSnippetsApiView, self).__init__(**kwargs)

    serializer_class      = DeleteSnippetSerializer
    response_schema_class = GetSnippetsDetailsCurrentUserApiSchema
    permission_classes    = (IsAuthenticated,)

    @swagger_auto_schema(tags   = ["Snippets"], request_body=serializer_class)
    def delete(self, request, *args, **kwargs):
        try: 
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                self.response_format['status_code']             = status.HTTP_400_BAD_REQUEST
                self.response_format["status"]                  = False
                self.response_format["errors"]                  = serializer.errors
                return Response(self.response_format, status    = status.HTTP_400_BAD_REQUEST)

            ids = serializer.validated_data.get('id',None)
            Snippet.objects.filter(id__in = ids).delete()
            snippet_instance = Snippet.objects.all().order_by('id')
            self.response_format['status_code']             = status.HTTP_200_OK
            self.response_format["data"]                    = self.response_schema_class(snippet_instance, many=True, context={'request': request}).data
            self.response_format["message"]                 = _success
            self.response_format["status"]                  = True
            return Response(self.response_format, status    = status.HTTP_200_OK)
            
        except Exception as e: 
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        

# Return all the Tags items
class GetTagListApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetTagListApiView, self).__init__(**kwargs)
    
    serializer_class    = GetTagListSchema
    permission_classes  = (IsAuthenticated,)
    pagination_class    = RestPagination
  
    @swagger_auto_schema(tags=["Tag"], pagination_class=RestPagination)
    def get(self, request):
        
        try:
            queryset    = Tag.objects.all().order_by('-id')
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
        

# Return the snippets corresponding to the tag with the use of tag id.
class GetTagDetailedApiView(generics.GenericAPIView):
    def __init__(self, **kwargs):
        self.response_format = ResponseInfo().response
        super(GetTagDetailedApiView, self).__init__(**kwargs)
        
    serializer_class = GetSnippetsDetailsCurrentUserApiSchema
    permission_classes = (IsAuthenticated,)

    id = openapi.Parameter('id', openapi.IN_QUERY, type=openapi.TYPE_STRING, required=True, description="Enter Tag id")
    
    @swagger_auto_schema(tags=["Tag"], manual_parameters=[id])
    def get(self, request):
        
        try:
            instance_id    = request.GET.get('id', None)

            filter_set = Q()
            if instance_id not in ['',None]:
                filter_set = Q(tag__id=instance_id)

            queryset    = Snippet.objects.filter(filter_set).order_by('-id')
            page        = self.paginate_queryset(queryset)
            serializer  = self.serializer_class(page, many=True, context={'request':request})
            return self.get_paginated_response(serializer.data)

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.response_format['status_code'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            self.response_format['status'] = False
            self.response_format['message'] = f'exc_type : {exc_type},fname : {fname},tb_lineno : {exc_tb.tb_lineno},error : {str(e)}'
            return Response(self.response_format, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
