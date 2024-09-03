from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from . import views
from django.contrib import messages
from .models import Room,Hall,Booking,NewsPost
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.

@login_required
def index(request):
    rooms = Room.objects.all()
    user_id = request.user.id  # Get the logged-in user's ID
    return render(request,"index.html", {'rooms': rooms})

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
        check_in_date = timezone.datetime.strptime(check_in_date, '%m/%d/%Y').date()
        check_out_date = timezone.datetime.strptime(check_out_date, '%m/%d/%Y').date()

        # Create the Booking
        Booking.objects.create(
            customer_name=customer_name,
            room=room,
            hall=hall,
            check_in_date=check_in_date,
            check_out_date=check_out_date,
            guests=int(guests),
            price=price 
        )

        # Redirect to a success page
        return redirect('booking_success')

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
      return render(request,'signup.html',context)
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
            return HttpResponse("Please fill all fields.", status=400)

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
    bookings = Booking.objects.all().order_by('-check_in_date') 
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
    return render(request, 'admin/booking.html', {'bookings': bookings})


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