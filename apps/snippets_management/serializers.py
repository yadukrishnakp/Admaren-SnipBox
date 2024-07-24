from rest_framework import serializers
from django.utils import timezone
from apps.snippets_management.models import Snippet, Tag
from snipbox_core.helpers.helper import get_token_user_or_none


# Collecting snippet details and save to database with unique tag name.
class CreateOrUpdateSnippetSerializer(serializers.ModelSerializer):
    title        = serializers.CharField(required=True)
    note         = serializers.CharField(required=True)
    tag          = serializers.CharField(required=True)

    class Meta:
        model = Snippet 
        fields = ['title','note','tag']
    
    
    def validate(self, attrs):
        return super().validate(attrs)

    
    def create(self, validated_data):
        request = self.context.get('request',None)
        user_instance = get_token_user_or_none(request)
        instance                = Snippet()
        instance.title          = validated_data.get('title')
        instance.note           = validated_data.get('note')
        instance.created_by     = user_instance
        instance.modified_by    = user_instance
        instance.created_date   = timezone.now()
        instance.modified_date  = timezone.now()
        instance.save()

        tag_instance, created = Tag.objects.get_or_create(title=validated_data.get('tag'))
        
        instance.tag = tag_instance

        instance.save()
        return instance
    


class UpdateSnippetserializer(serializers.Serializer):
    id           = serializers.IntegerField(required=True,allow_null=True)
    title        = serializers.CharField(required=True)
    note         = serializers.CharField(required=True)
    tag          = serializers.CharField(required=True)

    class Meta:
        model   = Snippet
        fields = ['id','title','note', 'tag']

    def validate(self, attrs):
        return super().validate(attrs)


    def update(self, instance, validated_data):
        request = self.context.get('request')
        user_instance = get_token_user_or_none(request)

        instance.title          = validated_data.get('title')
        instance.note           = validated_data.get('note')
        instance.modified_by    = user_instance
        instance.modified_date  = timezone.now()

        tag_instance, created = Tag.objects.get_or_create(title=validated_data.get('tag'))
        
        instance.tag = tag_instance
        instance.save()
        
        return instance