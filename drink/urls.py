from django.urls import path
import drink.views as drinkviews

urlpatterns = [
    path('releases', drinkviews.ReleasesView.as_view(), name='releases'),  
    path('submit-drink', drinkviews.SubmitDrinkView.as_view(), name='submit-drink'),  
    path('review-drink', drinkviews.ReviewDrinkView.as_view(), name='review-drink'),  
]
