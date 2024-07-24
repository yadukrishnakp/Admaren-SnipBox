from rest_framework import serializers

from apps.snippets_management.models import Snippet, Tag


# Return Snippets details as response with Hyperlink
class GetSnippentsListSchema(serializers.ModelSerializer):
    hyperlink         = serializers.SerializerMethodField('get_hyperlink')

    class Meta:
        model = Snippet
        fields = ['pk', 'title', 'note', 'hyperlink']

    # generating the hyperlink
    def get_hyperlink(self, instance):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(f'/api/snippents_management/get-snippet-details-current-user?id={instance.id}')
        return None
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    

# Return Snippets details as response.
class GetSnippentDetailedViewSchema(serializers.ModelSerializer):
    tag   = serializers.CharField(source="tag.title")

    class Meta:
        model = Snippet
        fields = ['pk', 'title', 'note', 'tag']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    

# Return Snippets details as response.
class GetSnippetsDetailsCurrentUserApiSchema(serializers.ModelSerializer):

    class Meta:
        model = Snippet
        fields = ['pk', 'title', 'note', 'created_date', 'modified_date']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas

# Return Snippets details as response, only if both current user and created user are same
class GetSnippetsDetailsCurrentUserApiSchema(serializers.ModelSerializer):

    class Meta:
        model = Snippet
        fields = ['pk', 'title', 'note', 'created_date', 'modified_date']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    

# Return snippets corresponding to the tag id.
class GetTagListSchema(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['pk', 'title']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas