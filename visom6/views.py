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

        if room_id:
            room = get_object_or_404(Room, id=room_id)
        elif hall_id:
            hall = get_object_or_404(Hall, id=hall_id)

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
            guests=int(guests)
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
        'hall': hall
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



def sig(request):
    return render(request, "admin/sign-in.html")