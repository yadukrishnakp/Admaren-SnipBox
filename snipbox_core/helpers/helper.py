import logging, json,socket
from django.contrib.auth import get_user_model
from django.utils import timezone
import math
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from apps.user.models import GeneratedAccessToken



logger = logging.getLogger(__name__)

# for find user with use of token
def get_token_user_or_none(request):
    User = get_user_model()
    try:
        instance = User.objects.get(id=request.user.id)
    except Exception:
        instance = None
    finally:
        return instance


def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.DoesNotExist:
        return None
    
