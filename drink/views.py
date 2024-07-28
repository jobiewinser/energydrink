import drink.models as drinkmodels
from django.db.models import Q
from typing import Any
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(login_required, name='dispatch')
class ReleasesView(TemplateView):
    template_name = "drink/releases.html"

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

@method_decorator(login_required, name='dispatch')
class SubmitDrinkView(TemplateView):
    template_name = "drink/submit_drink.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["brands"] = drinkmodels.DrinkBrand.objects.filter(
            Q(approved=True) | Q(submitted_by=self.request.user)
        )
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get("drink_name")
        if not name:
            return HttpResponse("Please enter a valid Drink Name", status=400)
        drink_brand_id = request.POST.get("drink_brand")
        if not drink_brand_id:
            return HttpResponse("Please select a valid Brand", status=400)
        drink = drinkmodels.Drink.objects.filter(
            Q(approved=True) | Q(submitted_by=request.user),
            name=name,
            drink_brand=drinkmodels.DrinkBrand.objects.get(pk=drink_brand_id),
        ).first()
        if not drink:
            drink = drinkmodels.Drink(
                name=name,
                drink_brand=drinkmodels.DrinkBrand.objects.get(pk=drink_brand_id),
                approved=False,
                submitted_by=request.user,
            )
            image = request.FILES.get("image")
            if image:
                drink.image = image
            drink.save()
        context = {
            "drink": drink,
        }
        return render(request, f"drink/htmx/view_drink_htmx.html", context)


@method_decorator(login_required, name='dispatch')
class SearchDrinksView(TemplateView):
    template_name = "drink/search_drinks.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["unapproved_drinks"] = drinkmodels.Drink.objects.filter(
            approved=False, submitted_by=self.request.user
        )
        context["drinks"] = drinkmodels.Drink.objects.filter(approved=True)
        return context

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ViewDrinkView(TemplateView):
    template_name = "drink/view_drink.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["drink"] = drinkmodels.Drink.objects.get(pk=kwargs["pk"])
        return context

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
