from django.urls import path
from . import views

urlpatterns = [

    # HOME

    path(
        '',
        views.home,
        name='home'
    ),

    # FLIGHT DETAILS

    path(
        'flight/<int:flight_id>/',
        views.flight_detail,
        name='flight_detail'
    ),

    # BOOK FLIGHT

    path(
        'book/<int:flight_id>/',
        views.book_flight,
        name='book_flight'
    ),

    # SEAT SELECTION

    path(
        'seat-selection/<int:flight_id>/',
        views.seat_selection,
        name='seat_selection'
    ),

    # CONFIRM BOOKING

    path(
        'confirm/<int:booking_id>/',
        views.confirm_booking,
        name='confirm_booking'
    ),

    # MY BOOKINGS

    path(
        'bookings/',
        views.my_bookings,
        name='my_bookings'
    ),

    # VIEW TICKET

    path(
        'view-ticket/<int:booking_id>/',
        views.view_ticket,
        name='view_ticket'
    ),

    # DOWNLOAD PDF TICKET

    path(
        'ticket/<int:booking_id>/',
        views.download_ticket,
        name='download_ticket'
    ),

    # DELETE / CANCEL BOOKING

    path(
        'delete-booking/<int:booking_id>/',
        views.delete_booking,
        name='delete_booking'
    ),

    # DASHBOARD

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    # REGISTER

    path(
        'register/',
        views.register,
        name='register'
    ),

    # LOGIN

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    # LOGOUT

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

]