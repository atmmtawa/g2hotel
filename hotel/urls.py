# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('book_room/<int:room_id>/', views.book_room, name='book_room'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('manage_bookings/', views.manage_bookings, name='manage_bookings'),
    path('add_room/', views.add_room, name='add_room'),
    path('room_list/', views.room_list, name='room_list'),
    path('', views.home, name='home'),
    path('room/<int:room_id>/', views.room_details, name='room_details'), 

]
