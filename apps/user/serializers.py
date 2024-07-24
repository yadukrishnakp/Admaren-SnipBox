import re
from rest_framework import serializers
from apps.user.models import  Users

# Save and Update collect informations of Users.
class CreateOrUpdateUserSerializer(serializers.ModelSerializer):
    user        = serializers.IntegerField(required=False,allow_null=True)
    username    = serializers.CharField(required=True)
    email       = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    password    = serializers.CharField(required=False)
    is_admin    = serializers.BooleanField(default=False)
    full_name   = serializers.CharField(required=False)
    
    class Meta:
        model = Users 
        fields = ['user','username','email','password','is_active','is_admin', 'full_name']
    
    
    # Checking the validations eg: Username, Password..
    def validate(self, attrs):
        email           = attrs.get('email', '')
        user            = attrs.get('user', None)
        username        = attrs.get('username', None)
        password        = attrs.get('password', None)
        user_query_set  = Users.objects.filter(email=email)

        if username is not None:
            if not re.match("^[a-zA-Z0-9._@]*$", username):
                raise serializers.ValidationError({'username':("Enter a valid Username. Only alphabets, numbers, '@', '_', and '.' are allowed.")})
            
        if user is not None:
            user_query_set = user_query_set.exclude(pk=user)
            
        if user_query_set.exists():
            raise serializers.ValidationError({"username":('Username already exists!')})
        
        if password is not None and (len(password) < 8 or not any(char.isupper() for char in password) or not any(char.islower() for char in password) or not any(char.isdigit() for char in password) or not any(char in '!@#$%^&*()_+-=[]{}|;:,.<>?\'\"\\/~`' for char in password)):
            raise serializers.ValidationError({"password":('Must Contain 8 Characters, One Uppercase, One Lowercase, One Number and One Special Character')})
            
        return super().validate(attrs)
    
    # Creation of Users
    def create(self, validated_data):
        password                  = validated_data.get('password')
        
        instance                  = Users()
        instance.username         = validated_data.get('username')
        instance.email            = validated_data.get('email')
        instance.full_name        = validated_data.get('full_name')
        instance.set_password(password) 
        instance.is_active        = validated_data.get('is_active')
        instance.is_admin         = validated_data.get('is_admin')
        instance.save()
        return instance
    
    # Updation of Users
    def update(self, instance, validated_data):
        password                  = validated_data.get('password','')
        instance.username         = validated_data.get('username')
        instance.email            = validated_data.get('email') 
        instance.full_name        = validated_data.get('full_name')
        instance.is_active        = validated_data.get('is_active')
        instance.is_admin         = validated_data.get('is_admin')
        if password:
            instance.set_password(password)
        instance.save()
        return instance