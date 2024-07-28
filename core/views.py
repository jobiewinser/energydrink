from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import redirect


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return redirect("search-drinks/")
