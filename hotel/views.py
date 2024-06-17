# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, GuestProfile, Booking, Room
from django.utils import timezone

def home(request):
    return render(request, "home.html")

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        
        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.is_guest = True
        user.save()
        
        GuestProfile.objects.create(user=user, phone_number=phone_number, address=address)
        login(request, user)
        return redirect('home')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def book_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == 'POST':
        check_in_date = request.POST['check_in_date']
        check_out_date = request.POST['check_out_date']
        number_of_guests = request.POST['number_of_guests']
        
        booking = Booking.objects.create(
            guest=request.user,
            room=room,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            number_of_guests=number_of_guests
        )
        return redirect('view_bookings')
    return render(request, 'book_room.html', {'room': room})

@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(guest=request.user)
    return render(request, 'view_bookings.html', {'bookings': bookings})

def room_list(request):
    rooms = Room.objects.all()
    room_statuses = []

    for room in rooms:
        # Check if there are any active bookings for the room
        now = timezone.now().date()
        is_booked = Booking.objects.filter(
            room=room,
            check_in_date__lte=now,
            check_out_date__gte=now
        ).exists()
        room_statuses.append({
            'room': room,
            'is_booked': is_booked
        })

    return render(request, 'room_list.html', {'room_statuses': room_statuses})

@login_required
def manage_bookings(request):
    if request.user.is_manager:
        bookings = Booking.objects.filter(room__hotel__managers__user=request.user)
        return render(request, 'manage_bookings.html', {'bookings': bookings})
    return redirect('home')
