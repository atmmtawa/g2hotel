# models.py
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('SINGLE', 'Single'),
        ('DOUBLE', 'Double'),
        ('SUITE', 'Suite'),
        ('FAMILY', 'Family'),
    ]

    hotel = models.ForeignKey(Hotel, related_name='rooms', on_delete=models.CASCADE, null=True)
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    room_image = models.FileField(upload_to="rooms/", null=True)
    max_number = models.IntegerField(default=4)

    def __str__(self):
        return f"{self.room_number} - {self.get_room_type_display()}"

class Booking(models.Model):
    guest = models.ForeignKey(CustomUser, related_name='bookings', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='bookings', on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.PositiveIntegerField()
    booking_date = models.DateTimeField(auto_now_add=True)
    is_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return f"Booking for {self.guest} in {self.room}"

class ManagerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, related_name='managers', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.get_full_name()
    
class StaffProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return self.user.get_full_name()
class CustomerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.get_full_name()

class GuestProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    gender = models.TextField(max_length=10, null=True)
    d_o_b = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.get_full_name()

class FoodItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='food_images/', blank=True, null=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    guest = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} by {self.guest}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.food_item.name} (Order {self.order.id})"