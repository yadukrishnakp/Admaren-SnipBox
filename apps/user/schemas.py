from rest_framework import serializers
from apps.user.models import  Users


# Return User details are Response
class GetUsersListApiSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['pk','username','email', 'full_name']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas
    
    
# Return User details are Response
class GetUsersDetailApiSerializers(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['pk','username','email', 'full_name','is_superuser','is_active','is_admin']
    
    def to_representation(self, instance):
        datas = super().to_representation(instance)
        for key in datas.keys():
            try:
                if datas[key] is None:
                    datas[key] = ""
            except KeyError:
                pass
        return datas