from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from utils.supabase_helpers import upload_to_supabase, get_supabase_client
from django.conf import settings

ROLES = [("organizer", "Organizer"), ("attendee", "Attendee")]

from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    image = serializers.FileField(
        required=False, write_only=True
    )  # Accept raw file uploads
    image_url = serializers.CharField(
        source="image", read_only=True
    )  # Expose the image URL

    class Meta:
        model = UserProfile
        fields = "__all__"

    def update(self, instance, validated_data):
        # Debugging: Check uploaded files and data
        print("FILES:", self.context["request"].FILES)  # Uploaded files
        print("DATA:", self.context["request"].data)  # Form data
        print("DATA:", validated_data)
        user_data = validated_data.get("user", {})
        instance.user.first_name = user_data.get("first_name", instance.user.first_name)
        instance.user.last_name = user_data.get("last_name", instance.user.last_name)
        instance.user.email = user_data.get("email", instance.user.email)
        instance.user.save()

        instance.receive_email_notifications = validated_data.get(
            "receive_email_notifications", instance.receive_email_notifications
        )
        instance.receive_in_app_notifications = validated_data.get(
            "receive_in_app_notifications", instance.receive_in_app_notifications
        )
        instance.notification_frequency = validated_data.get(
            "notification_frequency", instance.notification_frequency
        )
        print(instance)

        image = validated_data.pop("image", None)
        if image:
            # Get the Supabase client
            supabase_client = get_supabase_client()
            bucket_name = settings.SUPABASE_BUCKET

            # Check if the user already has an image URL stored
            old_image_path = None
            if instance.image:  # If an image already exists
                # Construct the old file path
                old_image_path = (
                    f"user_images/{instance.user.id}/{instance.image.split('/')[-1]}"
                )

            # Define the new file path
            file_path = f"user_images/{instance.user.id}/{image.name}"

            # Upload the image to Supabase (delete old one if necessary)
            image_url = upload_to_supabase(
                supabase_client, bucket_name, image, file_path, old_image_path
            )

            # Save the new image URL to the instance
            instance.image = image_url

        # Save the updated instance
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
