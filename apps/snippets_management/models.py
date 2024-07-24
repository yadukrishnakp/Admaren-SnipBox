from django.db import models
from snipbox_core.models import AbstractDateTimeFieldBaseModel
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from random import randint
# Create your models here.
    

class Tag(AbstractDateTimeFieldBaseModel):
    slug         = models.SlugField(_('Slug'), max_length=100, editable=False)
    title        = models.CharField(_('Tag Title'), unique=True, max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def save(self, *args, **kwargs):
        if not self.slug or self.title:
            self.slug = slugify(str(self.title))
            if Tag.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.title)) + '-' + str(randint(1, 9999999))
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.title)
    

class Snippet(AbstractDateTimeFieldBaseModel):
    slug         = models.SlugField(_('Slug'), max_length=100, editable=False)
    title        = models.CharField(_('Snippent Title'), max_length=255, blank=True, null=True)
    note         = models.TextField(_('Snippet Note'), blank=True, null=True)
    tag          = models.ForeignKey(Tag, related_name="snippet_tag", on_delete=models.CASCADE, null=True,blank=True)

    class Meta:
        verbose_name = 'Snippet'
        verbose_name_plural = 'Snippets'

    def save(self, *args, **kwargs):
        if not self.slug or self.title:
            self.slug = slugify(str(self.title))
            if Snippet.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = slugify(str(self.title)) + '-' + str(randint(1, 9999999))
        super(Snippet, self).save(*args, **kwargs)


    def __str__(self):
        return str(self.title)