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
    filterset_fields = ["category__slug", "organizer__id"]

    def get_queryset(self):
        queryset = super().get_queryset()

        # Get the tags__id parameter from the query string
        tags_param = self.request.query_params.get("tags__id", "")

        if tags_param:
            # Split the string by commas to get a list of tag IDs
            tags = tags_param.split(",")
            try:
                # Convert the list of strings to a list of integers
                tags = [int(tag_id) for tag_id in tags]
            except ValueError:
                # Handle cases where the tag IDs aren't valid integers
                raise ValueError("Tag IDs must be valid integers.")

            # Filter the queryset by the tag IDs
            queryset = queryset.filter(tags__id__in=tags).distinct()

        return queryset


class RSVPViewSet(viewsets.ModelViewSet):
    queryset = RSVP.objects.all()
    serializer_class = RSVPSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["event__id", "attendee__id", "is_accepted"]
