from django.contrib import admin
from visom6.models import Room,Booking,Hall,NewsPost,NewsCategory,Profile
# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    # Display the room type, price, total rooms, booked rooms, and available rooms
    list_display = ('room_type', 'price_per_night', 'total_rooms', 'booked_rooms_count', 'available_rooms_count')

    # Method to show booked rooms in admin
    def booked_rooms_count(self, obj):
        return obj.booked_rooms
    booked_rooms_count.short_description = 'Booked Rooms'

    # Method to show available rooms in admin
    def available_rooms_count(self, obj):
        return obj.available_rooms
    available_rooms_count.short_description = 'Available Rooms'
    
admin.site.register(Room,RoomAdmin)
admin.site.register(Hall)
admin.site.register(NewsPost)
admin.site.register(NewsCategory)
admin.site.register(Profile)
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'room', 'check_in_date', 'check_out_date', 'guests')