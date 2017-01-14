from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response

from mutual_funds.finance.models import Fund

from .serialisers import FundDetailSerializer, FundListSerializer


class FundDetailAPIView(RetrieveAPIView):
    queryset = Fund.objects.published()
    serializer_class = FundDetailSerializer


class FundListAPIView(ListAPIView):
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = "finance/api/list.html"
    serializer_class = FundListSerializer

    def get_queryset(self):
        queryset = Fund.objects.sort_by_return(days=self.request.query_params.get('days', 365))
        return queryset

    def get(self, request, *args, **kwargs):
        context = {
            'time_period_date': self.request.query_params.get('days', 365),
            'funds': self.get_queryset(),
        }
        return Response(context)
