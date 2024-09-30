from rest_framework import serializers
from .models import Category, Tag, Event, RSVP
from members.models import UserProfile
from django.contrib.auth.models import User
from .functions import attempt_json_deserialize
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class OrganizerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
        ]


class OrganizerProfileSerializer(serializers.ModelSerializer):
    user = OrganizerUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["user"]


class EventSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)
    organizer = OrganizerProfileSerializer(read_only=True)

    class Meta:
        model = Event
        fields = "__all__"

    def create(self, validated_data):
        request = self.context["request"]
        organizer_id = request.data.get("organizer")
        organizer, created = UserProfile.objects.get_or_create(pk=organizer_id)
        validated_data["organizer"] = organizer
        category_id = request.data.get("category")
        category, created = Category.objects.get_or_create(pk=category_id)
        validated_data["category"] = category
        tags_data = request.data.get("tags")
        tags = tags_data.split(",")
        # print(type(tags))
        tag_list = []
        # for tag in tags:

        #     t = Tag.objects.get_or_create(pk=tag)
        #     tag_list.append(t)
        validated_data["tags"] = tags

        print(validated_data, "line 54")
        instance = super().create(validated_data)

        return instance

    def update(self, instance, validated_data):
        print(validated_data)
        attendee_count = validated_data.get("attendee_count", 0)
        instance.attendee_count += attendee_count
        request = self.context["request"]
        print(type(request.data.get("tags")))
        category_id = request.data.get("category")
        if category_id:
            category, created = Category.objects.get_or_create(pk=category_id)
            instance.category = category
        tags_data = request.data.get("tags")
        print(tags_data)
        if tags_data:
            #     lst = tags_data[0]
            #     tags = lst.split(",")
            instance.tags.set(tags_data)
        instance.name = validated_data.get("name", instance.name)
        instance.date = validated_data.get("date", instance.date)
        instance.description = validated_data.get("description", instance.description)
        instance.time = validated_data.get("time", instance.time)
        instance.location = validated_data.get("location", instance.location)
        instance.thumbnail = validated_data.get("thumbnail")
        print(instance)
        instance.save()
        return instance


class RSVPEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            "id",
            "name",
            "date",
            "time",
            "location",
            "thumbnail",
        ]


class RSVPUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]


class RSVPAttendeeSerializer(serializers.ModelSerializer):
    user = RSVPUserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = ["id", "user", "image"]


class RSVPSerializer(serializers.ModelSerializer):
    event = RSVPEventSerializer(read_only=True)
    attendee = RSVPAttendeeSerializer(read_only=True)

    class Meta:
        model = RSVP
        fields = "__all__"

    def create(self, validated_data):
        request = self.context["request"]
        attendee_id = request.data.get("attendee")
        attendee, created = UserProfile.objects.get_or_create(pk=attendee_id)
        validated_data["attendee"] = attendee
        event_id = request.data.get("event")
        event, created = Event.objects.get_or_create(pk=event_id)
        validated_data["event"] = event

        instance = super().create(validated_data)

        return instance
