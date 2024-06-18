# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from django.utils import timezone
from .forms import StaffCreationForm

def landing_page(request):
    return render(request, 'landing_page.html')

@login_required
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
        gender = request.POST['gender']
        d_o_b = request.POST['d_o_b']
        
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
        
        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.is_guest = True
        user.save()
        
        GuestProfile.objects.create(user=user, d_o_b = d_o_b, gender=gender, phone_number=phone_number, address=address)
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
    return render(request, 'confirm_booking.html', {'room': room})

@login_required
def view_bookings(request):
    bookings = Booking.objects.filter(guest=request.user)
    return render(request, 'view_bookings.html', {'bookings': bookings})

@login_required
def room_list(request):
    rooms = Room.objects.all()
    room_statuses = []

    for room in rooms:
        # Check if there are any active bookings for the room
        now = timezone.now().date()
        is_booked = Booking.objects.filter(
            room=room,
            check_out_date__gte=now
        ).exists()
        print(is_booked)
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

@login_required
def add_room(request):
    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        price_per_night = request.POST.get('price_per_night')
        is_available = request.POST.get('is_available') == 'on'
        description = request.POST.get('description')
        image = request.FILES.get('image')
        
        if not room_number or not room_type or not price_per_night:
            messages.error(request, "Please fill out all required fields.")
            return redirect('add_room')
        
        room = Room(
            room_number=room_number,
            room_type=room_type,
            price_per_night=price_per_night,
            is_available=is_available,
            description=description,
            room_image=image
        )
        room.save()
        messages.success(request, "Room added successfully!")
        return redirect('room_list')
    
    return render(request, 'add_room.html')



def room_details(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    now = timezone.now().date()
    is_booked = Booking.objects.filter(
            room=room,
            check_out_date__gte=now
        ).exists()
    return render(request, 'room_details.html', {'room': room, 'is_booked': is_booked})

@login_required
def add_food_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_available = request.POST.get('is_available') == 'on'
        image = request.FILES.get('image')

        if not name or not price:
            messages.error(request, "Please fill out all required fields.")
            return redirect('add_food_item')

        food_item = FoodItem(
            name=name,
            description=description,
            price=price,
            is_available=is_available,
            image=image
        )
        food_item.save()
        messages.success(request, "Food item added successfully!")
        return redirect('food_menu')
    
    return render(request, 'add_food_item.html')

@login_required
def food_menu(request):
    food_items = FoodItem.objects.filter(is_available=True)
    if request.method == 'POST':
        food_item_ids = request.POST.getlist('food_items')
        quantities = request.POST.getlist('quantities')
        
        if not food_item_ids or not quantities:
            messages.error(request, "Please select at least one food item.")
            return redirect('food_menu')
        
        order = Order.objects.create(
            guest=request.user,
            total_price=0,
            is_processed=False
        )

        total_price = 0
        for food_item_id, quantity in zip(food_item_ids, quantities):
            if int(quantity) > 0:
                food_item = FoodItem.objects.get(id=food_item_id)
                quantity = int(quantity)
                order_item = OrderItem.objects.create(
                    order=order,
                    food_item=food_item,
                    quantity=quantity
                )
                total_price += food_item.price * quantity

        order.total_price = total_price
        order.save()
        
        messages.success(request, "Order placed successfully!")
        return redirect('view_orders')
    
    return render(request, 'food_menu.html', {'food_items': food_items})


@login_required
def view_orders(request):
    orders = Order.objects.filter(guest=request.user)
    return render(request, 'view_orders.html', {'orders': orders})

@login_required
def view_pending_orders(request):
    if not (request.user.is_staff or request.user.is_manager):
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')
    
    pending_orders = Order.objects.filter(is_processed=False)
    return render(request, 'pending_orders.html', {'orders': pending_orders})

@login_required
def confirm_order(request, order_id):
    if not (request.user.is_staff or request.user.is_manager):
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')

    order = get_object_or_404(Order, id=order_id)
    order.is_processed = True
    order.save()
    messages.success(request, "Order has been confirmed.")
    return redirect('view_pending_orders')

@login_required
def add_staff(request):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not email or not phone_number or not password1 or not password2:
            messages.error(request, "Please fill out all required fields.")
            return redirect('add_staff')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('add_staff')

        user = CustomUser.objects.create_user(username=username, email=email, password=password1)
        user.is_staff = True
        user.save()
        StaffProfile.objects.create(user=user, phone_number=phone_number)
        messages.success(request, "Staff user added successfully!")
        return redirect('staff_list')

    return render(request, 'add_staff.html')


@login_required
def staff_list(request):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')

    staff_members = CustomUser.objects.filter(is_staff=True)
    return render(request, 'staff_list.html', {'staff_members': staff_members})

@login_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        room_number = request.POST.get('room_number')
        room_type = request.POST.get('room_type')
        price_per_night = request.POST.get('price_per_night')
        is_available = request.POST.get('is_available') == 'on'
        description = request.POST.get('description')
        image = request.FILES.get('image')

        if not room_number or not room_type or not price_per_night:
            messages.error(request, "Please fill out all required fields.")
            return redirect('edit_room', room_id=room_id)

        room.room_number = room_number
        room.room_type = room_type
        room.price_per_night = price_per_night
        room.is_available = is_available
        room.description = description

        if image:
            room.image = image

        room.save()
        messages.success(request, "Room details updated successfully!")
        return redirect('room_list')

    return render(request, 'edit_room.html', {'room': room})

@login_required
def edit_food_item(request, food_item_id):
    food_item = get_object_or_404(FoodItem, id=food_item_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        is_available = request.POST.get('is_available') == 'on'
        image = request.FILES.get('image')

        if not name or not price:
            messages.error(request, "Please fill out all required fields.")
            return redirect('edit_food_item', food_item_id=food_item_id)

        food_item.name = name
        food_item.description = description
        food_item.price = price
        food_item.is_available = is_available

        if image:
            food_item.image = image

        food_item.save()
        messages.success(request, "Food item details updated successfully!")
        return redirect('food_menu')

    return render(request, 'edit_food_item.html', {'food_item': food_item})

@login_required
def all_orders(request):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')

    orders = Order.objects.all()
    return render(request, 'all_orders.html', {'orders': orders})

@login_required
def all_users(request):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to view this page.")
        return redirect('home')

    managers = CustomUser.objects.filter(is_manager=True).order_by('username')
    staff = CustomUser.objects.filter(is_staff=True, is_manager=False).order_by('username')
    guests = CustomUser.objects.filter(is_guest=True, is_staff=False, is_manager=False).order_by('username')
    
    users = list(managers) + list(staff) + list(guests)

    return render(request, 'all_users.html', {'users': users})

@login_required
def suspend_user(request, user_id):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')

    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, "User has been suspended.")
    return redirect('all_users')

@login_required
def resuspend_user(request, user_id):
    if not request.user.is_manager:
        messages.error(request, "You do not have permission to perform this action.")
        return redirect('home')

    user = get_object_or_404(CustomUser, id=user_id)
    user.is_active = True
    user.save()
    messages.success(request, "User has been Activated.")
    return redirect('all_users')

def edit_user(request):
    pass