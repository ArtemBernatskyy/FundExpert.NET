from django.http import Http404
from django.contrib import messages
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _

from mutual_funds.utils.mixins import UserAuthenticatedAccessMixin

from .models import Profile
from .forms import ProfileUpdateForm


class ProfileDetailView(UserAuthenticatedAccessMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'

    def get_object(self):
        if not Profile.objects.filter(slug=self.kwargs['slug']).exists() or self.request.user.profile != Profile.objects.get(slug=self.kwargs['slug']):
            raise Http404
        return self.get_queryset().get(slug=self.kwargs['slug'])


class ProfileUpdateView(UserAuthenticatedAccessMixin, UpdateView):
    template_name = 'accounts/update.html'
    form_class = ProfileUpdateForm

    def get_object(self):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(**kwargs)
        return context

    def get_success_url(self):
        messages.success(self.request, _('Profile updated successfully'))
        return reverse_lazy('accounts:profile_detail', kwargs={'slug': self.request.user.profile.slug})
