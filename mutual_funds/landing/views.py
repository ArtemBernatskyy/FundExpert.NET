from django.views.generic import TemplateView, DetailView

from mutual_funds.finance.models import Fund
from .models import NewsPost


class MainPageView(TemplateView):
    template_name = 'landing/main_page.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        context['news_posts'] = NewsPost.objects.published()
        context['funds'] = Fund.objects.sort_by_return(days=30)[:30]
        return context


class NewsDetailView(DetailView):
    model = NewsPost
    template_name = 'landing/news_page.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return NewsPost.objects.all()
        else:
            return NewsPost.objects.published()


class FAQView(TemplateView):
    template_name = 'landing/faq.html'


class AboutView(TemplateView):
    template_name = 'landing/about.html'
