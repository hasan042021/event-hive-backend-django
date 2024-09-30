from rest_framework import viewsets
from .serializers import (
    CategorySerializer,
    TagSerializer,
    EventSerializer,
    RSVPSerializer,
)
from .models import Category, Tag, Event, RSVP
from rest_framework import filters, pagination
from django_filters.rest_framework import DjangoFilterBackend
import django_filters


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["category__slug", "tags__id", "organizer__id"]

    # def get_queryset(self):
    #     queryset = Event.objects.all()
    #     tags_list = self.request.GET.getlist("tags")
    #     if tags_list:
    #         lst = tags_list[0]
    #         lst_str = lst.split(",")
    #         for tag in lst_str:
    #             queryset = queryset.filter(tags__id__in=tag)

    #     return queryset


class RSVPViewSet(viewsets.ModelViewSet):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["event__id", "attendee__id", "is_accepted"]
