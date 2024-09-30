from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User

ROLES = [("organizer", "Organizer"), ("attendee", "Attendee")]

from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = "__all__"

    def update(self, instance, validated_data):
        user_data = validated_data.get("user", {})
        instance.user.first_name = user_data.get("first_name", instance.user.first_name)
        instance.user.last_name = user_data.get("last_name", instance.user.last_name)
        instance.user.email = user_data.get("email", instance.user.email)
        instance.user.save()

        instance.image = validated_data.get("image", instance.image)
        instance.receive_email_notifications = validated_data.get(
            "receive_email_notifications", instance.receive_email_notifications
        )
        instance.receive_in_app_notifications = validated_data.get(
            "receive_in_app_notifications", instance.receive_in_app_notifications
        )
        instance.notification_frequency = validated_data.get(
            "notification_frequency", instance.notification_frequency
        )
        instance.save()

        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required=True)
    role = serializers.ChoiceField(choices=ROLES)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "confirm_password",
            "role",
        ]

    def save(self):
        username = self.validated_data["username"]
        first_name = self.validated_data["first_name"]
        last_name = self.validated_data["last_name"]
        email = self.validated_data["email"]
        password = self.validated_data["password"]
        password2 = self.validated_data["confirm_password"]
        role = self.validated_data["role"]

        if password != password2:
            raise serializers.ValidationError({"error": "Passwords do not match."})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email Already exists"})
        account = User(
            username=username, email=email, first_name=first_name, last_name=last_name
        )
        account.set_password(password)
        account.is_active = False
        account.save()
        UserProfile.objects.create(user=account, role=role)
        return account


class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile

        fields = ["id", "role"]


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class UserPasswordChangeSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)
