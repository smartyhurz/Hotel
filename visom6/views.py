from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login,logout
from . import views
from django.contrib import messages
from .models import Room,Hall,Booking,NewsPost
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.timezone import now
from django.urls import reverse
from django.db.models import Sum
from .models import Room, Hall, Booking 
# Create your views here.


def index(request):
    rooms = Room.objects.all()
    user_id = request.user.id  # Get the logged-in user's ID
    return render(request,"index.html", {'rooms': rooms})


def custom_logout_view(request):
    logout(request)
    return redirect('/index/')

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'room_detail.html', {'room': room})

def about(request):
    return render(request,"about.html")

def dashboard_view(request):
     bookings = Booking.objects.filter(customer_name=request.user.username)  # Adjust according to your model
     return render(request, 'dashboard.html', {'bookings': bookings})


def booking_success(request):
    return render(request, 'booking_success.html')

def banquet(request):
    halls = Hall.objects.all()  # Retrieve all hall instances
    return render(request, 'banquet.html', {'halls': halls})

'''def booking_view(request,room_id=None, hall_id=None):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        hall_id = request.POST.get('hall_id')
        customer_name = request.POST.get('customer_name')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        guests = request.POST.get('adults')  # assuming 'adults' represents total guests

        room = None
        hall = None

        if room_id:
            room = get_object_or_404(Room, id=room_id)
        elif hall_id:
            hall = get_object_or_404(Hall, id=hall_id)
            
        context = {
        'room': room,
        'hall': hall
    }    

        # Assuming dates are in 'YYYY-MM-DD' format
        check_in_date = timezone.datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out_date = timezone.datetime.strptime(check_out_date, '%Y-%m-%d').date()

        # Create the Booking
        booking = Booking.objects.create(
            customer_name=customer_name,
            room=room,
            hall=hall,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            guests=int(guests)
        )
        booking.save()

        # Redirect to a success page or the same page with a success message
        return redirect('booking_success')  # Replace with the actual URL name

    return render(request, 'book.html',context)'''
@login_required(login_url='/login/')
def booking_view(request, room_id=None, hall_id=None):
    if request.method == 'POST':
        room_id = request.POST.get('room_id')
        hall_id = request.POST.get('hall_id')
        customer_name = request.POST.get('customer_name')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        guests = request.POST.get('adults')  # assuming 'adults' represents total guests

        room = None
        hall = None
        price = 0.00  # Initialize price
       # if room_id:
        #    room = get_object_or_404(Room, id=room_id)
        #elif hall_id:
         #   hall = get_object_or_404(Hall, id=hall_id)
        if room_id:
            try:
                room = Room.objects.get(id=room_id)
                price = room.price_per_night 
            except Room.DoesNotExist:
                room = None
        elif hall_id:
            try:
                hall = Hall.objects.get(id=hall_id)
                price = hall.price_per_night
            except Hall.DoesNotExist:
                hall = None   
                
        if not room and not hall:
          return render(request, 'book.html', {'error': 'Invalid room or hall ID.'})        
        # Convert dates from string to date object
        check_in_date = timezone.datetime.strptime(check_in_date, '%Y-%m-%d').date()
        check_out_date = timezone.datetime.strptime(check_out_date, '%Y-%m-%d').date()

        # Create the Booking
        booking = Booking.objects.create(
            customer_name=customer_name,
            room=room,
            hall=hall,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            guests=int(guests),
            price=price, 
            payment_status='pending'
        )

        # Redirect to a success page
        return redirect(reverse('payment', args=[booking.id]))

    # Handle GET request or form rendering
    room = None
    hall = None

    if room_id:
        room = get_object_or_404(Room, id=room_id)
    elif hall_id:
        hall = get_object_or_404(Hall, id=hall_id)

    context = {
        'room': room,
        'hall': hall,
        'price': room.price_per_night if room else (hall.price_per_night if hall else 0.00)
    }

    return render(request, 'book.html', context)

def club(request):
    return render(request,"club.html")


def contact(request):
    return render(request,"contact.html")

def news(request):
    return render(request,"news.html")

def rest(request):
    return render(request,"restaurant.html")

def rooms(request):
    rooms = Room.objects.all()
    user_id = request.user.id  # Get the logged-in user's ID
    return render(request,"rooms.html", {'rooms': rooms})

def spa(request):
    return render(request,"spa-wellness.html")

def error(request):
    return render(request,"404.html")

def login(request):
    return render(request,"login.html")
        
def register(request):
  context={}
  if request.method == 'POST':
    username = request.POST["uname"]
    usermail= request.POST["uemail"]
    password=request.POST["upass"]
    confirmpass=request.POST["ucpass"]
    
    if username=="" or password=="" or confirmpass=="" or usermail=="":
      context['errmsg']="Fields cannot be empty"
      return render(request, "signup.html",context)
    else:
      u=User.objects.create(password=password,username=username,email=usermail)
      u.set_password(password) #hashing the password
      u.save()
      context['success']="Succesfully Registered"
      return redirect('/login/',context)
  else: 
     return render(request,'signup.html',context)
 

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Validate username and password are not empty
        if not username or not password:
            return render(request, 'login.html', {'errmsg': 'Email and password are required.'})

        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        # Check if authentication was successful
        if user is not None:
            auth_login(request, user)
            # Redirect to a success page after login
            return redirect('/index/')
        else:
            # Return an 'invalid login' error message
            return render(request, 'login.html', {'errmsg': 'Invalid Email or password.'})
    else:
        return render(request, 'login.html')        
     

def check_rooms(request):
    if request.method == 'POST':
        check_in = request.POST.get('check_in')
        check_out = request.POST.get('check_out')
        persons = request.POST.get('persons')
        room_type = request.POST.get('room_type')
        rooms = request.POST.get('rooms')

        # Validate the data as needed
        if not (check_in and check_out and persons and room_type and rooms):
            return render(request, 'index.html')

        # Check room availability
        available_rooms = check_room_availability(check_in, check_out, room_type, rooms)
        
        if available_rooms:
            return render(request, 'rooms_available.html', {'available_rooms': available_rooms})
        else:
            return render(request, 'no_rooms_available.html')

    return render(request, 'booking_form.html')

def check_room_availability(check_in, check_out, room_type, rooms):
    # Logic to check room availability based on the input data
    # This function should return a list of available rooms or None if none are available
    pass



def news_list(request):
    news_posts = NewsPost.objects.all().order_by('-publication_date')
    context = {
        'news_posts': news_posts,
    }
    return render(request, 'news.html', context)


#admin view
from django.contrib.auth.decorators import user_passes_test
from django.utils.timezone import now
from django.db.models import Sum,F,ExpressionWrapper,FloatField

def sig(request):
    return render(request, "admin/sign-in.html")

def sigu(request):
    return render(request, "admin/sign-up.html")

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def superuser_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            auth_login(request, user)
            return redirect('addash/')  # Redirect to Django admin
        else:
            return render(request, 'admin/sign-in.html', {'error': 'Invalid credentials or not a superuser'})
    return render(request, 'admin/sign-in.html')



def dash(request):
    today = now().date()
    
    todays_users_count = User.objects.filter(date_joined__date=today).count()
    todays_money = Booking.objects.filter(check_in_date=today).aggregate(total=Sum('price'))['total']
    total_users = User.objects.count()
    total_sales = Booking.objects.aggregate(total=Sum('price'))['total'] or 0
    rooms = Room.objects.all()
    halls = Hall.objects.all()
    bookings = Booking.objects.all().order_by('check_in_date') 
    context = {
        'todays_users_count': todays_users_count,
        'todays_money': todays_money if todays_money else 0,
        'total_users': total_users,
        'total_sales': total_sales,
        'rooms': rooms,
        'halls': halls,
        'bookings': bookings,
    }
    return render(request,"admin/dashboard.html",context)


@user_passes_test(lambda u: u.is_superuser)
def profile(request):
    rooms = Room.objects.all()
    halls = Hall.objects.all()
    context = {
        'rooms': rooms,
        'halls': halls,
        'user': request.user  # Pass the user object to the template
    }
    return render(request, 'admin/profile.html',context)

def tables(request):
    users = User.objects.all()
    return render(request,"admin/tables.html", {'users': users})


# Edit user
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.is_superuser = 'is_superuser' in request.POST
        user.save()
        return redirect('/tables/')
    return render(request, 'admin/edit.html', {'user': user})


# Delete user
@login_required
def delete_user(request, item_type, item_id):
    if item_type == 'user':
        item = get_object_or_404(User, id=item_id)
        redirect_url = '/tables/'  # Change this to your user list view name
    elif item_type == 'booking':
        item = get_object_or_404(Booking, id=item_id)
        redirect_url = 'booking_list'
    elif item_type == 'room':
        item = get_object_or_404(Room, id=item_id)
        redirect_url = 'room_list'  # Change this to your room list view name
    elif item_type == 'hall':
        item = get_object_or_404(Hall, id=item_id)
        redirect_url = 'hall_list'  # Change this to your hall list view name
    else:
        return redirect('/tables/')  # Redirect to home or another page if type is invalid

    if request.method == "POST":
        item.delete()
        messages.success(request, f"{item_type.capitalize()} deleted successfully.")
        return redirect(redirect_url)

    context = {
        'item': item,
        'item_type': item_type,
    }
    return render(request, 'admin/delete.html', context)


def booking_list(request):
    bookings = Booking.objects.all()
    filter_type = request.GET.get('filter', 'all')  # Default to 'all' if no filter is selected

    rooms = Room.objects.all()
    bookings = Booking.objects.select_related('room')
    total_rooms = sum(room.available_rooms + room.booked_rooms for room in rooms)
    
    #available_rooms = [room for room in rooms if room.available_rooms > 0]
    #booked_rooms = [room for room in rooms if room.booked_rooms > 0]
    total_available_rooms = sum(room.available_rooms for room in rooms)
    total_booked_rooms = sum(room.booked_rooms for room in rooms)
    
    if filter_type == 'available':
        filtered_rooms = [room for room in rooms if room.available_rooms > 0]
    elif filter_type == 'booked':
        filtered_rooms = [room for room in rooms if room.booked_rooms > 0]
        #filtered_rooms = available_rooms
    #elif filter_type == 'booked':
        #filtered_rooms = booked_rooms
    else:
        filtered_rooms = rooms

    context = {
        'rooms': filtered_rooms,
        'total_rooms': total_rooms,
        'bookings': bookings,
        #'available_rooms': len(available_rooms),
        #'booked_rooms': len(booked_rooms),
        'bookings': bookings,
        'available_rooms': total_available_rooms,  # Total count of available rooms
        'booked_rooms': total_booked_rooms,  
    }
    return render(request, 'admin/booking.html',context)

def reset_booked_rooms(request):
    rooms = Room.objects.all()
    for room in rooms:
        room.booked_rooms = 0
        room.save()
    messages.success(request, 'Successfully reset booked rooms for all rooms.')
    return redirect('booking_list')  # Redirect to any view after resetting


def edit_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    rooms = Room.objects.all()
    halls = Hall.objects.all()
    
    if request.method == "POST":
        # Update the booking details with POST data
        booking.customer_name = request.POST.get('customer_name')
        room_id = request.POST.get('room')
        hall_id = request.POST.get('hall')
        check_in_date1 = request.POST.get('check_in_date')
        check_out_date1 = request.POST.get('check_out_date')
        booking.guests = request.POST.get('number_of_guests')
        booking.price = request.POST.get('price')
        
        booking.guests = int(request.POST.get('number_of_guests'))
        booking.price = float(request.POST.get('price'))
        
         # Assuming the date format from the form is 'mm/dd/yyyy'
        booking.check_in_date = timezone.datetime.strptime(check_in_date1, '%m-%d-%Y').date()
        booking.check_out_date = timezone.datetime.strptime(check_out_date1, '%m-%d-%Y').date()
       
        if room_id:
            booking.room = Room.objects.get(id=room_id)
            booking.hall = None
        elif hall_id:
            booking.hall = Hall.objects.get(id=hall_id)
            booking.room = None
        
        booking.save()
        
        return redirect('booking_list')  # Redirect to a success page or back to the booking list

    context = {
        'booking': booking,
        'rooms': rooms,
        'halls': halls
    }
    return render(request, 'admin/editbook.html',context)

def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == 'POST':
        booking.delete()
        return redirect('booking_list')
    return render(request, 'booking_confirm_delete.html', {'booking': booking})

def rooomhall(request):
    rooms = Room.objects.all()
    halls = Hall.objects.all() 
    context = {
        'rooms': rooms,
        'halls': halls,
    }
    return render(request,"admin/roomadmin.html",context)

def edit_item(request, item_type, item_id):
    if item_type == 'room':
        item = get_object_or_404(Room, id=item_id)
        redirect_url = 'room_list'
        item_name = 'Room'
    elif item_type == 'hall':
        item = get_object_or_404(Hall, id=item_id)
        redirect_url = 'hall_list'
        item_name = 'Hall'
    else:
        return redirect('home')  # Redirect to a default page if item_type is invalid

    if request.method == 'POST':
        if item_type == 'room':
            item.room_type = request.POST.get('room_type')
            item.price_per_night = request.POST.get('price_per_night')
            item.description = request.POST.get('description')
            if 'image' in request.FILES:
                item.image = request.FILES['image']
        elif item_type == 'hall':
            item.hall_type = request.POST.get('hall_type')
            item.price_per_night = request.POST.get('price_per_night')
            item.description = request.POST.get('description')
            if 'image' in request.FILES:
                item.image = request.FILES['image']
        
        item.save()
        return redirect(rooomhall)  # Redirect after saving changes

    context = {
        'item': item,
        'item_type': item_type,
        'item_name': item_name
    }
    return render(request, 'admin/editroom.html', context)



########## PAYMENT ##########

# views.py
import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from .models import Booking, Payment
from django.views.decorators.csrf import csrf_exempt

# Initialize Razorpay client
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def payment_view(request,booking_id):
        booking = Booking.objects.get(id=booking_id)

        # Create Razorpay order
        razorpay_order = razorpay_client.order.create({
            "amount":  int(booking.price * 100),  # Convert to paise (cents)
            "currency": "INR",
            "payment_capture": "1"
        })
        
        # Pass the order_id and other data to the template
        context = {
        "razorpay_order_id": razorpay_order['id'],
        "razorpay_key_id": settings.RAZORPAY_KEY_ID,
        "amount": booking.price,
        "booking_id": booking_id,
        }

        return render(request, 'payment.html',context)


@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        razorpay_order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        try:
            # Verify the payment signature
            razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            })

            # Save the payment to the database
            Payment.objects.create(
                razorpay_payment_id=payment_id,
                razorpay_order_id=razorpay_order_id,
                amount=request.POST.get('amount'),
            )

            return render(request, 'payment_success.html')

        except razorpay.errors.SignatureVerificationError:
            return render(request, 'payment_error.html')

    return redirect('payment_view')
