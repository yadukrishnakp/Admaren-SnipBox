from django.db import models
from snipbox_core.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
# Create your models here.
    

class Tag(models.Model):
    title         = models.CharField(_('Tag Title'), unique=True, max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return str(self.title)
    

class Snippet(AbstractDateTimeFieldBaseModel):
    title        = models.CharField(_('Snippent Title'), max_length=255, blank=True, null=True)
    note         = models.TextField(_('Snippet Note'), blank=True, null=True)
    tag          = models.ForeignKey(Tag, related_name="snippet_tag", on_delete=models.CASCADE, null=True,blank=True)

    class Meta:
        verbose_name = 'Snippet'
        verbose_name_plural = 'Snippets'


    def __str__(self):
        return str(self.title)