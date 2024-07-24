
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import gettext_lazy as _




class UserManager(BaseUserManager):
    def create_user(self, username, password = None, **extra_fields):
        if not username:
            raise ValueError(_('The username must be set'))

        user = self.model(username = username, **extra_fields)
        if password:
            user.set_password(password.strip())
            
        user.save()
        return user


    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
     
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser = True.'))
        
        return self.create_user(username, password, **extra_fields)



class Users(AbstractBaseUser):

    email                         = models.EmailField(_('email'), unique = True, max_length = 255, blank = True, null = True)
    full_name                     = models.CharField(_('name'), max_length=255, blank = True, null = True)
    username                      = models.CharField(_('username'), max_length = 300, unique = True, blank = True, null = True)
    password                      = models.CharField(_('password'), max_length=255, blank = True, null = True)
    date_joined                   = models.DateTimeField(_('date_joined'),  auto_now_add = True, blank = True, null = True)
    is_admin                      = models.BooleanField(default = False)
    is_superuser                  = models.BooleanField(default = False)
    is_active                     = models.BooleanField(_('Is Active'), default=True)
    
    
    

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    objects = UserManager()
    
    def __str__(self):
        return "{username}".format(username=self.username)


class GeneratedAccessToken(models.Model):
    token = models.TextField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.token


    
    
