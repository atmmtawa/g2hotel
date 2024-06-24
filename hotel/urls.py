# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('book_room/<int:room_id>/', views.book_room, name='book_room'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),    
    path('all_bookings/', views.all_bookings, name='all_bookings'),
    path('manage_bookings/', views.manage_bookings, name='manage_bookings'),
    path('rooms/add/', views.add_room, name='add_room'),
    path('room_list/', views.room_list, name='room_list'),
    path('home/', views.home, name='home'),
    path('', views.landing_page, name="landing_page"),
    path('room/<int:room_id>/', views.room_details, name='room_details'), 
    path('add_food_item/', views.add_food_item, name='add_food_item'),
    path('food_menu/', views.food_menu, name='food_menu'), 
    path('view_orders/', views.view_orders, name='view_orders'),
    path('pending_orders/', views.view_pending_orders, name='view_pending_orders'),  # Added URL pattern for viewing pending orders
    path('confirm_order/<int:order_id>/', views.confirm_order, name='confirm_order'),
    path('add_staff/', views.add_staff, name='add_staff'),  # Added URL pattern for adding staff
    path('staff_list/', views.staff_list, name='staff_list'),  # Added URL pattern for viewing orders
    path('edit_room/<int:room_id>/', views.edit_room, name='edit_room'),  # Added URL pattern for editing room
    path('edit_food_item/<int:food_item_id>/', views.edit_food_item, name='edit_food_item'),  # Added URL pattern for editing food item
    path('all_orders/', views.all_orders, name='all_orders'),
    path('all_users/', views.all_users, name='all_users'),  # Added URL pattern for viewing all users
    path('suspend_user/<int:user_id>/', views.suspend_user, name='suspend_user'),  
    path('resuspend_user/<int:user_id>/', views.resuspend_user, name='resuspend_user'),  
    path('delete_food_item/<int:food_item_id>/', views.delete_food_item, name='delete_food_item'),
    path('delete_room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('view_user_details/<int:user_id>/', views.view_user_details, name='view_user_details'),  # View user details
    path('edit_user/<int:user_id>/', views.edit_user, name='edit_user'), 
    path('order_details/<int:order_id>/', views.order_details, name='order_details'), 
    path('room_booking_details/<int:booking_id>/', views.room_booking_details, name='room_booking_details'),# Edit user details
    path('confirm_booking/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
        path('food_item_details/<int:food_item_id>/', views.food_item_details, name='food_item_details'),  # Food item details
]
