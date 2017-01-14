import os
from uuid import uuid4

from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.utils.deconstruct import deconstructible
from django.utils.translation import ugettext_lazy as _

from slugify import UniqueSlugify
from imagekit.processors import Adjust
from imagekit.processors import ResizeToFill
from imagekit.models import ProcessedImageField
from django_countries.fields import CountryField

from mutual_funds.finance.models import Fund


@deconstructible
class UploadToPathAndRename(object):
    '''
        Here we are renaming photos with uuid in order to not overwrite previous photo
    '''
    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(uuid4().hex, ext)
        return os.path.join(self.sub_path, filename)


class Profile(models.Model):
    SEX_CHOICES = (
        (1, _('man')),
        (0, _('woman')),
        (None, _("don't show"))
    )
    user = models.OneToOneField(User, related_name='profile')
    avatar_thumbnail = ProcessedImageField(upload_to=UploadToPathAndRename('avatars'),
                                           processors=[ResizeToFill(400, 400), Adjust(sharpness=1.1, contrast=1.1)],
                                           format='JPEG',
                                           options={'quality': 90}, null=True, blank=True)
    sex = models.IntegerField(choices=SEX_CHOICES, blank=True, null=True, verbose_name=_('gender'))
    slug = models.SlugField(unique=True, max_length=100)
    birthday = models.DateField(null=True, blank=True, verbose_name=_('birthday'))
    country = CountryField(blank=True, null=True, blank_label=_('(select country)'))
    liked_funds = models.ManyToManyField(Fund, through='LikedFund')

    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def show_liked_funds(self):
        return self.liked_funds.all()

    def image_thumb(self):
        if self.avatar_thumbnail:
            return '<img src="{0}{1}" width="100" height="100" />'.format(settings.MEDIA_URL, self.avatar_thumbnail)
        else:
            return '<img src="{0}accounts/default/default-avatar.jpg" width="100" height="100" />'.format(settings.STATIC_URL)
    image_thumb.allow_tags = True

    def get_absolute_url(self):
        return reverse('accounts:profile_detail', kwargs={'slug': self.slug})

    def get_avatar(self):
        if self.avatar_thumbnail:
            return self.avatar_thumbnail.url
        else:
            return '{}accounts/default/default-avatar.jpg'.format(settings.STATIC_URL)

    def __str__(self):
        return self.user.username


def my_unique_check(text, uids):
    if text in uids:
        return False
    return not Profile.objects.filter(slug=text).exists()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        slugify_unique = UniqueSlugify(
            unique_check=my_unique_check,
            separator='_',
            to_lower=True,
            max_length=100
        )
        slug = slugify_unique(instance.username)
        Profile.objects.create(user=instance, slug=slug)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class LikedFund(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'fund']
