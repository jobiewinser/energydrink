import drink.models as drinkmodels
from django.db.models import Q, Count
from typing import Any
from django.views.generic import TemplateView
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django_countries import countries
import core.models as coremodels


# @method_decorator(login_required, name="dispatch")
class EditDrinkView(TemplateView):
    template_name = "drink/edit_drink.html"

    def get_context_data(self, pk=None, **kwargs: Any) -> dict[str, Any]:
        if self.request.META.get("HTTP_HX_REQUEST", "false") == "true":
            self.template_name = "drink/htmx/edit_drink_htmx.html"
        context = super().get_context_data(**kwargs)
        context["brands"] = drinkmodels.Brand.objects.filter(
            Q(approved=True) | Q(submitted_by=self.request.user)
        )
        if pk:
            context["drink"] = drinkmodels.Drink.objects.get(pk=pk)
        return context

    def post(self, request, pk=None, *args, **kwargs):
        if pk:
            if request.user.is_superuser:
                drink = drinkmodels.Drink.objects.get(
                    pk=pk,
                )
            else:
                drink = drinkmodels.Drink.objects.get(
                    Q(approved=True) | Q(submitted_by=request.user),
                    pk=pk,
                )
        else:
            drink = drinkmodels.Drink(
                submitted_by=request.user,
                approved=True,
            )
        name = request.POST.get("drink_name")
        if not name:
            return HttpResponse("Please enter a valid Drink Name", status=400)
        brand_id = request.POST.get("brand")
        if not brand_id:
            return HttpResponse("Please select a valid Brand", status=400)
        caffeine_per_hundred_ml = request.POST.get("caffeine_per_hundred_ml") or None
        drink.name = name.strip()
        brand = drinkmodels.Brand.objects.get(pk=brand_id)
        drink.brand = brand
        image = request.FILES.get("image")
        if image:
            drink.image = request.FILES.get("image")
        drink.caffeine_per_hundred_ml = caffeine_per_hundred_ml
        matching_drinks = drinkmodels.Drink.objects.filter(
            Q(approved=True) | Q(submitted_by=request.user),
            name=name,
            brand=brand,
            caffeine_per_hundred_ml=caffeine_per_hundred_ml,
        )
        if pk:
            matching_drinks = matching_drinks.exclude(pk=pk)
        if matching_drinks.exists():
            return HttpResponse("We already have a record of this drink", status=400)
        drink.save()
        context = {
            "drink": drink,
        }
        return render(request, f"drink/htmx/view_drink_htmx.html", context)


@method_decorator(login_required, name="dispatch")
class ReviewDrinkView(TemplateView):
    template_name = "drink/review_drink.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if self.request.META.get("HTTP_HX_REQUEST", "false") == "true":
            self.template_name = "drink/htmx/review_drink_htmx.html"
        context = super().get_context_data(**kwargs)
        drink = drinkmodels.Drink.objects.get(pk=kwargs["pk"])
        context["drink"] = drink
        context["countries"] = dict(countries)
        context["currencies"] = coremodels.CURRENCIES
        context["review"] = drinkmodels.Review.objects.filter(
            submitted_by=self.request.user,
            drink=drink,
        ).first()
        return context

    def post(self, request, *args, **kwargs):
        taste = request.POST["taste"]
        if not taste:
            return HttpResponse("Please rate the Taste", status=400)
        pk = kwargs["pk"]
        drink = drinkmodels.Drink.objects.get(pk=pk)
        title = (request.POST["title"] or "").strip()
        description = (request.POST["description"] or "").strip()
        country_purchased = request.POST["country_purchased"] or None
        price_paid = request.POST["price_paid"] or None
        currency = request.POST["currency"] or None
        image = request.FILES.get("image") or None

        review, created = drinkmodels.Review.objects.get_or_create(
            submitted_by=request.user,
            drink=drink,
        )

        review.taste = taste
        review.title = title
        review.description = description
        review.image = image
        review.country_purchased = country_purchased
        review.price_paid = price_paid
        review.currency = currency
        review.save()
        response = HttpResponse(status=200)
        response["HX-Redirect"] = f"/reviews/{drink.pk}/"
        return response


# @method_decorator(login_required, name="dispatch")
class ReviewsView(TemplateView):
    template_name = "drink/reviews.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if self.request.META.get("HTTP_HX_REQUEST", "false") == "true":
            self.template_name = "drink/htmx/reviews_htmx.html"
        context = super().get_context_data(**kwargs)
        drink = drinkmodels.Drink.objects.get(pk=kwargs["pk"])
        context["drink"] = drink
        if self.request.user.is_authenticated:
            context["reviews"] =  drink.review_drink.exclude(submitted_by=self.request.user)
            context["user_reviews"] =  drink.review_drink.filter(
                submitted_by=self.request.user
            )
        else:
            context["reviews"] = drink.review_drink.all()
            context["user_reviews"] = drink.review_drink.none()
        return context


class ListDrinksView(TemplateView):
    template_name = "drink/list_drinks.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if self.request.META.get("HTTP_HX_REQUEST", "false") == "true":
            self.template_name = "drink/htmx/list_drinks_htmx.html"
        context = super().get_context_data(**kwargs)
        view = self.request.GET.get("view")
        if not view:
            is_mobile = self.request.user_agent.is_mobile
            if is_mobile:
                view = "list"
            else:
                view = "gallery"
        context["view"] = view
        context["brands"] = drinkmodels.Brand.objects.all()
        context["show_filters"] = self.request.GET.get("show_filters") == "true"

        return context


def search_drinks(request):
    context = {}

    if request.META.get("HTTP_HX_REQUEST", "false") == "false":
        # Extract all query parameters
        query_dict = request.GET

        # Reverse the URL for the list-drinks view
        list_drinks_url = reverse("list-drinks")

        # Add the query parameters to the URL
        url_with_params = f"{list_drinks_url}?{query_dict.urlencode()}"

        # Redirect to the constructed URL
        return redirect(url_with_params)
    view = request.GET.get("view")
    if not view:
        is_mobile = request.user_agent.is_mobile
        if is_mobile:
            view = "list"
        else:
            view = "gallery"
    context["view"] = view
    template_name = f"drink/htmx/search_drinks_{view}_htmx.html"
    taste = request.GET.get("taste")
    caffeine_per_hundred_ml = request.GET.get("caffeine_per_hundred_ml")
    sort = request.GET.get("sort")
    brand = request.GET.get("brand")
    search = (request.GET.get("search") or "").strip()

    # if request.user.id:
    #     context["unapproved_drinks"] = drinkmodels.Drink.objects.filter(
    #         approved=False, submitted_by=request.user
    #     )
    drinks = drinkmodels.Drink.objects.all()
    if not request.user.is_superuser:
        drinks = drinks.filter(approved=True)
    if taste:
        drinks = drinks.filter(average_taste__gte=taste)
    if caffeine_per_hundred_ml:
        drinks = drinks.filter(caffeine_per_hundred_ml__gte=caffeine_per_hundred_ml)
    if sort:
        if "review_drink" in sort:
            drinks = drinks.annotate(count=Count("review_drink"))
            if sort == "review_drink__count":
                drinks = drinks.order_by("count")
            elif sort == "-review_drink__count":
                drinks = drinks.order_by("-count")
        else:
            drinks = drinks.order_by(sort)
    if brand:
        drinks = drinks.filter(brand__id=brand)
    if search:
        drinks = drinks.filter(
            Q(name__icontains=search) | Q(brand__name__icontains=search)
        )
    context["drinks"] = drinks
    return render(request, template_name, context)


class ViewDrinkView(TemplateView):
    template_name = "drink/view_drink.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        if self.request.META.get("HTTP_HX_REQUEST", "false") == "true":
            self.template_name = "drink/htmx/view_drink_htmx.html"
        context = super().get_context_data(**kwargs)
        context["drink"] = drinkmodels.Drink.objects.get(pk=kwargs["pk"])
        return context

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
