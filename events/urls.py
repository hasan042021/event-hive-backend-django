from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register("tags", views.TagViewSet)
router.register("categories", views.CategoryViewSet)
router.register("list", views.EventViewSet)
router.register("rsvp-list", views.RSVPViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
