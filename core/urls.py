from django.urls import path
import core.views as coreviews

urlpatterns = [
    path("", coreviews.HomeView.as_view(), name="home"),
    path("accounts/profile/", coreviews.ProfileView.as_view(), name="profile"),
    path("logout", coreviews.logout_func, name="logout"),
    # path('accounts/register/', coreviews.RegisterNewCompanyView.as_view(), name='register'),
]
