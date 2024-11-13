from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register("profiles", views.UserProfileViewSet, basename="member")
urlpatterns = [
    path("", include(router.urls)),
    path("register/", views.UserRegistrationApiView.as_view(), name="register"),
    path("login/", views.UserLoginApiView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("change_password/", views.ChangePasswordView.as_view(), name="change_pass"),
    path("active/<uid64>/<token>/", views.activate, name="activate"),
    path("activated/", views.AcivatedView.as_view(), name="activated"),
]
