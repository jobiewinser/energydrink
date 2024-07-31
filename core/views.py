from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django_countries import countries
import core.models as coremodels


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return redirect("search-drinks/")


@method_decorator(login_required, name="dispatch")
class ProfileView(TemplateView):
    template_name = "core/profile.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["countries"] = dict(countries)
        context["currencies"] = coremodels.CURRENCY_CHOICES
        profile, created = coremodels.Profile.objects.get_or_create(user=self.request.user)
        context["profile"] = profile
        return context

    def post(self, request, *args, **kwargs):
        profile = self.request.user.profile        
        profile.display_name = request.POST['display_name']
        profile.country = request.POST['country']
        profile.currency = request.POST['currency']
        profile.save()
        return redirect("profile")


def logout_func(request):
    logout(request)
    return redirect("login")
