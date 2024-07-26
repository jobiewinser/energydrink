from django.urls import path
import core.views as coreviews

urlpatterns = [
    path("", coreviews.HomeView.as_view(), name="home"),
    # path('accounts/register/', coreviews.RegisterNewCompanyView.as_view(), name='register'),
]
