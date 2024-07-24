from rest_framework import serializers
from apps.user.models import Users



class LoginResponseSchema(serializers.ModelSerializer):
    
    class Meta:
        model = Users
        fields = [
            "id",
            "email",
            "username",
            "is_active",
            "is_superuser",
        ]