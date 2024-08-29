from django.contrib import admin
from visom6.models import Room,Booking,Hall,NewsPost,NewsCategory
# Register your models here.
admin.site.register(Room)
admin.site.register(Hall)
admin.site.register(NewsPost)
admin.site.register(NewsCategory)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'room', 'check_in_date', 'check_out_date', 'guests')