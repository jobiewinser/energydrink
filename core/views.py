from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django_countries import countries
import core.models as coremodels
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db.models import Q


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return redirect("list-drinks")


@method_decorator(login_required, name="dispatch")
class ProfileView(TemplateView):
    template_name = "core/profile.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if self.request.META.get("HTTP_HX_REQUEST", "false") == "true":
            self.template_name = "core/htmx/profile_htmx.html"
        context = super().get_context_data(**kwargs)
        context["countries"] = dict(countries)
        context["currencies"] = coremodels.CURRENCY_CHOICES
        profile, created = coremodels.Profile.objects.get_or_create(
            user=self.request.user
        )
        if created:
            profile.display_name = self.request.user.username
            profile.country = "GB"
            profile.currency = "GBP"
            profile.save()
        context["profile"] = profile
        context["show_saved"] = self.request.GET.get("saved")
        return context

    def post(self, request, *args, **kwargs):
        display_name = request.POST["display_name"]
        if (
            coremodels.Profile.objects.exclude(user=request.user)
            .filter(display_name=display_name)
            .exists()
        ):
            return HttpResponse("This name is already taken", status=400)
        profile = self.request.user.profile
        profile.display_name = request.POST["display_name"]
        profile.country = request.POST["country"]
        profile.currency = request.POST["currency"]
        profile.save()
        response = HttpResponse(status=200)
        response["HX-Redirect"] = "/accounts/profile/?saved=true"
        return response


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if self.request.META.get("HTTP_HX_REQUEST", "false") == "true":
            self.template_name = "registration/htmx/register_htmx.html"
        context = super().get_context_data(**kwargs)
        context["next"] = self.request.GET.get("next")
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        try:
            validate_email(email)
        except ValidationError as e:
            return HttpResponse("This email is invalid", status=400)
        if User.objects.filter(email=email).exists():
            return HttpResponse("This email is already taken", status=400)
        password = request.POST["password"]
        password_confirm = request.POST["password_confirm"]
        if password != password_confirm:
            return HttpResponse("Your passwords do not match", status=400)
        if len(password) < 8:
            return HttpResponse(
                "The new password must be at least 8 characters long", status=400
            )
        user = User.objects.create_user(email, email=email, password=password)
        login(request, user)
        response = HttpResponse(status=200)
        response["HX-Redirect"] = request.POST.get("next") or "/accounts/profile/"
        return response


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if self.request.META.get("HTTP_HX_REQUEST", "false") == "true":
            self.template_name = "registration/htmx/login_htmx.html"
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        email = request.POST["email"]
        password = request.POST["password"]
        user = User.objects.filter(Q(email=email) | Q(username=email)).first()
        if user and user.check_password(password):
            login(request, user)
            response = HttpResponse(status=200)
            response["HX-Redirect"] = request.POST.get("next") or "/accounts/profile/"
            return response
        response = HttpResponse("Incorrect Email or Password", status=401)
        return response


@login_required
def logout_func(request):
    logout(request)
    return redirect("login")
