from django import forms
from django.forms.models import model_to_dict, fields_for_model
from django.contrib.auth.models import User
from django_countries.widgets import CountrySelectWidget
from django.utils.translation import ugettext_lazy as _

from .models import Profile


class ProfileUpdateForm(forms.ModelForm):

    def __init__(self, instance=None, *args, **kwargs):
        _fields = ('first_name', 'last_name', 'email',)
        _initial = model_to_dict(instance.user, _fields) if instance is not None else {}
        kwargs.update(initial=_initial)
        super(ProfileUpdateForm, self).__init__(instance=instance, *args, **kwargs)
        self.fields.update(fields_for_model(User, _fields))

    class Meta(object):
        model = Profile

        fields = (
            'country',
            'sex',
            'birthday',
            'avatar_thumbnail',
        )

        widgets = {
            'country': CountrySelectWidget(),
            'birthday': forms.SelectDateWidget(
                years=list(reversed(range(1901, 2002))),
                empty_label=(_("Year"), _("Month"), _("Day")),
                attrs=({'style': 'width: 32%; display: inline-block;'})),
            'avatar_thumbnail': forms.FileInput(),
            'sex': forms.RadioSelect(),
        }

    def save(self, *args, **kwargs):
        u = self.instance.user
        u.first_name = self.cleaned_data['first_name']
        u.last_name = self.cleaned_data['last_name']
        u.save()
        profile = super(ProfileUpdateForm, self).save(*args, **kwargs)
        return profile
