from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.base import TemplateView


class IndexTemplateView(TemplateView):
    def get_template_names(self):
        template_name = "index.html"
        return template_name


@ensure_csrf_cookie
def single_page_view(request):
    return render(request, "index.html")


def terms_of_use_view(request):
    return render(request, "terms_of_use.html")


def privacy_policy_view(request):
    return render(request, "privacy_policy.html")


def embed_view(request):
    return render(request, 'embed.html')
