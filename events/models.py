from django.db import models
from members.models import UserProfile
from django.contrib.auth.models import User


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name}"


class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    thumbnail = models.ImageField(upload_to="events/images/", null=True, blank=True)

    description = models.TextField()

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True
    )
    tags = models.ManyToManyField(Tag, related_name="events")
    is_public = models.BooleanField(default=True)
    organizer = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="events"
    )
    attendee_count = models.IntegerField(default=0)
    is_declined = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.id} {self.name}"


class RSVP(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    attendee = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    is_accepted = models.BooleanField(default=False)
    is_declined = models.BooleanField(default=False)

    def __str__(self):
        return f"Event Name : {self.event.name} - Attendee : {self.attendee.user.first_name}"
