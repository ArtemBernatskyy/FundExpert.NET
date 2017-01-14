import os
import uuid

from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from imagekit.processors import Adjust
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from imagekit.models import ImageSpecField
from ckeditor_uploader.fields import RichTextUploadingField


class NewsCategory(models.Model):
    title = models.CharField(
        max_length=250,
        help_text='Maximum 250 characters.'
    )
    slug = models.SlugField(
        unique=True,
        help_text=_('Suggested value automatically generated from title. '
                    'Must be unique.')
    )

    class Meta:
        ordering = ['title']
        verbose_name_plural = "News categories"

    def __str__(self):
        return self.title


@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)


class NewsPostQuerySet(models.QuerySet):
    def published(self):
        return self.active().filter(pub_date__lte=timezone.now())

    def active(self):
        return self.filter(is_active=True)


class NewsPost(models.Model):
    title = models.CharField(db_index=True, max_length=150)
    slug = models.SlugField(unique=True, max_length=200)
    is_active = models.BooleanField(
        help_text=_(
            "Tick to make this entry live (see also the publication date). "
            "Note that administrators (like yourself) are allowed to preview "
            "inactive entries whereas the general public aren't."
        ),
        default=False,
    )
    pub_date = models.DateTimeField(
        verbose_name=_("Publication date"),
        help_text=_(
            "For an entry to be published, it must be active and its "
            "publication date must be in the past."
        ),
    )
    image = ProcessedImageField(
        upload_to=UploadToPathAndRename('news'),
        processors=[ResizeToFill(1000, 616), Adjust(sharpness=1.1, contrast=1.1)],
        format='JPEG',
        options={'quality': 90},
        null=True,
    )

    category = models.ManyToManyField(NewsCategory, related_name='posts')
    text = RichTextUploadingField()

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    objects = NewsPostQuerySet.as_manager()

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('landing:detail', kwargs={'slug': self.slug})

    image_thumbnail = ImageSpecField(
        source='image',
        processors=[ResizeToFill(300, 168)],
        format='JPEG',
        options={'quality': 80}
    )

    def get_latest_news(self):
        return NewsPost.objects.exclude(pk=self.pk)[:3]
