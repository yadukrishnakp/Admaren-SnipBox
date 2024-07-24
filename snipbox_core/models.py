from django.db import models
from safedelete import SOFT_DELETE_CASCADE
from safedelete.models import SafeDeleteModel
from django.utils.translation import gettext_lazy as _
from apps.user.models import Users

class AbstractDateTimeFieldBaseModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE
    
    created_by    = models.ForeignKey(Users, on_delete=models.SET_NULL, related_name='%(class)s_created', null=True, blank=True)
    modified_by   = models.ForeignKey(Users, on_delete=models.SET_NULL, related_name='%(class)s_modified', null=True, blank=True)
    created_date  = models.DateTimeField(_('created_date'), auto_now_add=True, editable=False, blank=True, null=True)
    modified_date = models.DateTimeField(_('modified_date'), auto_now=True, editable=False, blank=True, null=True)
    is_active     = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
