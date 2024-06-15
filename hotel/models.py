from django.db import models
from django.contrib.auth.models import User

# Define a model for Hotel
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.name

# Define a model for Room
class Room(models.Model):
    ROOM_TYPES = [
        ('S', 'Single'),
        ('D', 'Double'),
        ('Q', 'Queen'),
        ('K', 'King'),
    ]
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=1, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.room_number} - {self.get_room_type_display()}'

# Define a model for Guest
class Guest(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)

    def __str__(self):
        return self.user.username

# Define a model for Reservation
class Reservation(models.Model):
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Reservation {self.id} by {self.guest.user.username}'

# Define a model for Service
class Service(models.Model):
    SERVICE_TYPES = [
        ('RS', 'Room Service'),
        ('CL', 'Cleaning'),
        ('LB', 'Laundry'),
        ('FW', 'Food & Beverages'),
    ]
    name = models.CharField(max_length=255)
    service_type = models.CharField(max_length=2, choices=SERVICE_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# Define a model for Service Request
class ServiceRequest(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    request_time = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.service.name} for Reservation {self.reservation.id}'
