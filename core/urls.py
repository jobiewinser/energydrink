from django.urls import path
import core.views as coreviews

urlpatterns = [
    path("", coreviews.HomeView.as_view(), name="home"),
    path("accounts/profile/", coreviews.ProfileView.as_view(), name="profile"),
    path("logout/", coreviews.logout_func, name="logout"),
    path("register/", coreviews.RegisterView.as_view(), name="register"),
    path("login/", coreviews.LoginView.as_view(), name="login"),
    path('change-theme/', coreviews.change_theme, name='change-theme'),
    # path('accounts/register/', coreviews.RegisterNewCompanyView.as_view(), name='register'),
]
