from django.db import models
from django.contrib.auth.models import User
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
    room = models.ForeignKey(Room, on_delete=models.CASCADE,blank=True, null=True)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, blank=True, null=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    guests = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2, editable=False,default=0.00)

    def save(self, *args, **kwargs):
        # Calculate the number of days
        days = (self.check_out_date - self.check_in_date).days

        # Calculate total price based on room or hall
        if self.room:
            self.price = days * self.room.price_per_night
        elif self.hall:
            self.price = days * self.hall.price_per_night

        super().save(*args, **kwargs)

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
    
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='default.jpg')
    job_title = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    mobile = models.CharField(max_length=15, blank=True)
    location = models.CharField(max_length=100, blank=True)    
    
    def __str__(self):
      return f'{self.user.username} Profile'