from django.db import models
from django.contrib.auth.models import User

ROLES = [("organizer", "Organizer"), ("attendee", "Attendee")]
FREQUENCY = [("daily", "Daily"), ("weekly", "Weekly"), ("monthly", "Monthly")]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLES)
    models.URLField(null=True, blank=True)
    receive_email_notifications = models.BooleanField(default=True)
    receive_in_app_notifications = models.BooleanField(default=True)
    notification_frequency = models.CharField(
        max_length=20, choices=FREQUENCY, default="daily"
    )

    def __str__(self):
        return f"Name:{self.user.first_name} {self.user.last_name}, id: {self.id}"
