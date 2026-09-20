from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from administration.permissions import Is_Counselor


class Home(LoginRequiredMixin, Is_Counselor, TemplateView):
    template_name = "administration/admin_home.html"
