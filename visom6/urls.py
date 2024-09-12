from django.contrib import admin
from django.urls import include
from django.urls import path
from visom6 import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('index/',views.index),
    path('about/',views.about),
    path('banquet/',views.banquet),
    path('club/',views.club),
    path('contact/',views.contact),
    path('login/',views.user_login),
    path('news/',views.news_list),
    path('restuarant/',views.rest),  
    path('rooms/',views.rooms,name='rooms'),
    path('signup/',views.register),
    path('spa/',views.spa),
    path('check-rooms/', views.check_rooms, name='check_rooms'),
    path('room/<int:room_id>/', views.room_detail, name='room_detail'),
    path('booking/room/<int:room_id>/', views.booking_view, name='booking_room'),
    path('booking/hall/<int:hall_id>/', views.booking_view, name='booking_hall'),
    path('booking_success/', views.booking_success, name='booking_success'), 
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
    path('dashboard/',views.dashboard_view),
    path('superuser-login/', views.superuser_login, name='superuser_login'),
    path('sigu/',views.sigu),
    path('superuser-login/addash/',views.dash),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='admin/sign-in.html'), name='login'),
    path('profile/',views.profile),
    path('tables/',views.tables,name='userf'),
    path('edit/<int:user_id>/', views.edit_user, name='edit'),
    path('reset-booked-rooms/', views.reset_booked_rooms, name='reset_booked_rooms'),
    
    path('bookin/', views.booking_list, name='booking_list'),

    # Update an existing booking
    path('bookin/<int:booking_id>/edit/', views.edit_booking, name='booking_update'),

    # Delete a booking
   
    path('delete/<str:item_type>/<int:item_id>/', views.delete_user, name='booking_delete'),
    
    path('roomhall/',views.rooomhall,name='roomhall'),
    path('edit/<str:item_type>/<int:item_id>/', views.edit_item, name='edit_item'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
