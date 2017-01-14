from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext as _
from django.http import HttpResponse, QueryDict
from mutual_funds.utils.mixins import UserAuthenticatedAccessMixin

from mutual_funds.accounts.models import LikedFund


class ChangeLikedFundView(UserAuthenticatedAccessMixin, View):
    def put(self, request, *args, **kwargs):
        try:
            fund_id = int(QueryDict(request.body).get('fund_id'))
            LikedFund(user=request.user.profile, fund_id=fund_id).save()
            return HttpResponse("successfully liked fund")
        except Exception as e:
            return HttpResponse("some error occured")

    def delete(self, request, *args, **kwargs):
        try:
            fund_id = int(QueryDict(request.body).get('fund_id'))
            found = LikedFund.objects.get(user=request.user.profile, fund__id=fund_id)
            found.delete()
            return HttpResponse("successfully unliked fund")
        except ObjectDoesNotExist:
            return HttpResponse("some error occured")
