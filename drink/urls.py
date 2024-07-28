from django.urls import path
import drink.views as drinkviews
import drink.htmx as drinkhtmx

urlpatterns = [
    path("releases/", drinkviews.ReleasesView.as_view(), name="releases"),
    path(
        "submit-drink-brand/", drinkhtmx.submit_drink_brand, name="submit-drink-brand"
    ),
    path("submit-drink/", drinkviews.SubmitDrinkView.as_view(), name="submit-drink"),
    path("search-drinks/", drinkviews.SearchDrinksView.as_view(), name="search-drinks"),
    path("view-drink/<int:pk>/", drinkviews.ViewDrinkView.as_view(), name="view-drink"),
]
