from rest_framework import serializers

from apps.snippets_management.models import Snippet


class GetSnippentsListSchema(serializers.ModelSerializer):
    hyperlink         = serializers.SerializerMethodField('get_hyperlink')

    class Meta:
        model = Snippet
        fields = ['pk', 'title', 'note', 'hyperlink']

    
    def get_hyperlink(self, instance):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(f'/api/snippents_management/get-count-and-details-list?id={instance.id}')
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