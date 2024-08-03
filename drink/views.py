import drink.models as drinkmodels
from django.db.models import Q, Count
from typing import Any
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django_countries import countries
import core.models as coremodels


@method_decorator(login_required, name="dispatch")
class ReleasesView(TemplateView):
    template_name = "drink/releases.html"

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class SubmitDrinkView(TemplateView):
    template_name = "drink/edit_drink.html"

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
                # approved=False, this will be false when going live
                approved=True,
                submitted_by=request.user,
                caffeine_per_hundred_ml=request.POST.get("caffeine_per_hundred_ml"),
            )
            image = request.FILES.get("image")
            if image:
                drink.image = image
            drink.save()
        context = {
            "drink": drink,
        }
        return render(request, f"drink/htmx/view_drink_htmx.html", context)


@method_decorator(login_required, name="dispatch")
class EditDrinkView(TemplateView):
    template_name = "drink/edit_drink.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["brands"] = drinkmodels.DrinkBrand.objects.filter(
            Q(approved=True) | Q(submitted_by=self.request.user)
        )
        context["drink"] = drinkmodels.Drink.objects.get(pk=kwargs["pk"])
        return context

    def post(self, request, *args, **kwargs):
        if request.user.is_superuser:
            drink = drinkmodels.Drink.objects.get(
                pk=kwargs["pk"],
            )

        drink = drinkmodels.Drink.objects.get(
            Q(approved=True) | Q(submitted_by=request.user),
            pk=kwargs["pk"],
        )
        name = request.POST.get("drink_name")
        if not name:
            return HttpResponse("Please enter a valid Drink Name", status=400)
        drink_brand_id = request.POST.get("drink_brand")
        if not drink_brand_id:
            return HttpResponse("Please select a valid Brand", status=400)

        drink.name = name
        drink.drink_brand = drinkmodels.DrinkBrand.objects.get(pk=drink_brand_id)
        image = request.FILES.get("image")
        if image:
            drink.image = request.FILES.get("image")
        drink.caffeine_per_hundred_ml = request.POST.get("caffeine_per_hundred_ml")
        drink.save()
        context = {
            "drink": drink,
        }
        return render(request, f"drink/htmx/view_drink_htmx.html", context)


@method_decorator(login_required, name="dispatch")
class ReviewDrinkView(TemplateView):
    template_name = "drink/review_drink.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        drink = drinkmodels.Drink.objects.get(pk=kwargs["pk"])
        context["drink"] = drink
        context["countries"] = dict(countries)
        context["currencies"] = coremodels.CURRENCY_CHOICES
        context["review"] = drinkmodels.Review.objects.filter(
            submitted_by=self.request.user,
            drink=drink,
        ).first()
        return context

    def post(self, request, *args, **kwargs):
        taste = request.POST["taste"]
        if not taste:
            return HttpResponse("Please rate the Taste", status=400)
        aftertaste = request.POST["aftertaste"]
        if not aftertaste:
            return HttpResponse("Please rate the Aftertaste", status=400)
        pk = kwargs["pk"]
        drink = drinkmodels.Drink.objects.get(pk=pk)
        title = request.POST["title"] or None
        description = request.POST["description"] or None
        country_purchased = request.POST["country_purchased"] or None
        price_paid = request.POST["price_paid"] or None
        currency = request.POST["currency"] or None
        currency = request.POST["currency"] or None
        image = request.FILES.get("image") or None

        review, created = drinkmodels.Review.objects.get_or_create(
            submitted_by=request.user,
            drink=drink,
        )

        review.taste = taste
        review.aftertaste = aftertaste
        review.title = title
        review.description = description
        review.image = image
        review.country_purchased = country_purchased
        review.price_paid = price_paid
        review.currency = currency
        review.save()
        response = HttpResponse(status=200)
        response["HX-Redirect"] = f"/search-drinks/"
        return response


@method_decorator(login_required, name="dispatch")
class ReviewsView(TemplateView):
    template_name = "drink/reviews.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["drink"] = drinkmodels.Drink.objects.get(pk=kwargs["pk"])
        return context


@method_decorator(login_required, name="dispatch")
class SearchDrinksView(TemplateView):
    template_name = "drink/search_drinks.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if self.request.META.get("HTTP_HX_REQUEST", "false") == "true":
            view = self.request.GET.get("view", "gallery")
            self.template_name = f"drink/htmx/search_drinks_{view}_htmx.html"
        context = super().get_context_data(**kwargs)
        context["unapproved_drinks"] = drinkmodels.Drink.objects.filter(
            approved=False, submitted_by=self.request.user
        )
        drinks = drinkmodels.Drink.objects.all()
        if not self.request.user.is_superuser:
            drinks = drinks.filter(approved=True)

        context["drink_brands"] = drinkmodels.DrinkBrand.objects.all()
        taste = self.request.GET.get("taste")
        aftertaste = self.request.GET.get("aftertaste")
        sort = self.request.GET.get("sort")
        drink_brand = self.request.GET.get("drink_brand")
        search = self.request.GET.get("search")
        if taste:
            drinks = drinks.filter(average_taste__gte=taste)
        if aftertaste:
            drinks = drinks.filter(average_aftertaste__gte=aftertaste)
        if sort:
            if "review_drink" in sort:
                drinks = drinks.annotate(count=Count("review_drink"))
                if sort == "review_drink__count":
                    drinks = drinks.order_by("count")
                elif sort == "-review_drink__count":
                    drinks = drinks.order_by("-count")
            else:
                drinks = drinks.order_by(sort)
        if drink_brand:
            drinks = drinks.filter(drink_brand__id=drink_brand)
        if search:
            drinks = drinks.filter(
                Q(name__icontains=search) | Q(drink_brand__name__icontains=search)
            )
        context["drinks"] = drinks
        return context

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@method_decorator(login_required, name="dispatch")
class ViewDrinkView(TemplateView):
    template_name = "drink/view_drink.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["drink"] = drinkmodels.Drink.objects.get(pk=kwargs["pk"])
        return context

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
