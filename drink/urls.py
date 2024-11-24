from django.urls import path
import drink.views as drinkviews
import drink.htmx as drinkhtmx

urlpatterns = [
    path(
        "submit-drink-brand/", drinkhtmx.submit_brand, name="submit-drink-brand"
    ),
    path("edit-drink/", drinkviews.EditDrinkView.as_view(), name="edit-drink"),
    path("edit-drink/<int:pk>/", drinkviews.EditDrinkView.as_view(), name="edit-drink"),
    # path("submit-drink/", drinkviews.SubmitDrinkView.as_view(), name="submit-drink"),
    path("list-drinks/", drinkviews.ListDrinksView.as_view(), name="list-drinks"),
    path("search-drinks/", drinkviews.search_drinks, name="search-drinks"),
    path("view-drink/<int:pk>/", drinkviews.ViewDrinkView.as_view(), name="view-drink"),
    path(
        "review-drink/<int:pk>/",
        drinkviews.ReviewDrinkView.as_view(),
        name="review-drink",
    ),
    path(
        "reviews/<int:pk>/",
        drinkviews.ReviewsView.as_view(),
        name="reviews",
    ),
]
