from django.contrib import messages
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.core.exceptions import PermissionDenied


class UserAuthenticatedAccessMixin(object):
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated():
            messages.warning(request, _('To perform this action necessary authorization'))
            return redirect(reverse('auth_login'))

        if not user.is_active:
            messages.warning(request, _('To perform this action necessary authorization'))
            raise PermissionDenied(_('To perform this action necessary authorization'))

        return super().dispatch(request, *args, **kwargs)
