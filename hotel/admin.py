from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Hotel)
admin.site.register(GuestProfile)
admin.site.register(ManagerProfile)
admin.site.register(Room)
admin.site.register(Booking)
# admin.site.register()
# admin.site.register()
