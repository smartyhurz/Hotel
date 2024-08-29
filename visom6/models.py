from django.db import models

# Create your models here.
class Room(models.Model):
    ROOM_TYPES = [
        ('junior_suite', 'Junior Suite'),
        ('family_room', 'Family Room'),
        ('double_room', 'Double Room'),
        ('deluxe_room', 'Deluxe Room'),
        ('superior_room', 'Superior Room'),
    ]

    room_type = models.CharField(max_length=20, choices=ROOM_TYPES, unique=True)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image1 = models.ImageField(upload_to='rooms/', blank=True, null=True)
    image2= models.ImageField(upload_to='rooms/', blank=True, null=True)
    max_persons = models.IntegerField()

    def __str__(self):
        return f"{self.get_room_type_display()} - ${self.price_per_night} per night"


class Hall(models.Model):
    BANQUET_TYPES = [
        ('birthday_hall', 'Birthday Celebration'),
        ('family_hall', 'Family Room'),
        ('office_hall', 'Office Conference'),
        ('social_hall', 'Social Events'),
        ('wedding_hall', 'Wedding Celebratiion'),
    ]

    hall_type = models.CharField(max_length=20, choices=BANQUET_TYPES, unique=True)
    price_per_night = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='halls/', blank=True, null=True)
    image1 = models.ImageField(upload_to='halls/', blank=True, null=True)
    image2= models.ImageField(upload_to='halls/', blank=True, null=True)
    max_persons = models.IntegerField()

    def __str__(self):
        return f"{self.get_hall_type_display()} - ${self.price_per_night} per night"


class Booking(models.Model):
    customer_name = models.CharField(max_length=100)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, blank=True, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField()

    def __str__(self):
        if self.room:
            return f"Booking for {self.customer_name} in {self.room}"
        elif self.hall:
            return f"Booking for {self.customer_name} in {self.hall}"
        else:
            return f"Booking for {self.customer_name}"
    


class NewsCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publication_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='news_images/')
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news_posts')

    def __str__(self):
        return self.title