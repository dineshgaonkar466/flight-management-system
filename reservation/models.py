from django.db import models
from django.contrib.auth.models import User


class Flight(models.Model):

    flight_number = models.CharField(max_length=10)

    origin = models.CharField(max_length=100)

    destination = models.CharField(max_length=100)

    departure_time = models.DateTimeField()

    arrival_time = models.DateTimeField()

    total_seats = models.PositiveIntegerField()

    available_seats = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    price = models.IntegerField(default=5000)

    def save(self, *args, **kwargs):

        if not self.pk or self.available_seats is None:

            self.available_seats = self.total_seats

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.flight_number}: {self.origin} → {self.destination}"


# SEAT MODEL

class Seat(models.Model):

    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE
    )

    seat_number = models.CharField(max_length=5)

    seat_type = models.CharField(max_length=10)

    is_booked = models.BooleanField(default=False)

    def __str__(self):

        return f"{self.flight.flight_number} - {self.seat_number}"


# BOOKING MODEL

class Booking(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE
    )

    seats_booked = models.PositiveIntegerField(default=1)

    seat_number = models.CharField(max_length=100)

    total_price = models.IntegerField(default=0)

    booking_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return f"{self.user.username} - {self.flight.flight_number}"