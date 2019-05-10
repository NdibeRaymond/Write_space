from django.views import generic
from django.urls import reverse_lazy,reverse


class LandingPage(generic.RedirectView):


    def get_redirect_url(self):
        return reverse("posts:post_list")


class aboutView(generic.TemplateView):
    template_name="about.html"
