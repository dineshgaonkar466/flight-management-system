from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Flight, Booking, Seat
from django.http import HttpResponse

from django.template.loader import get_template
from xhtml2pdf import pisa

import random


def home(request):
    flights = Flight.objects.all()

    source = request.GET.get('source')
    destination = request.GET.get('destination')

    if source and destination:
        flights = Flight.objects.filter(
            origin__icontains=source,
            destination__icontains=destination
        )

    return render(request, 'home.html', {'flights': flights})


def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    return render(request, 'flight_detail.html', {'flight': flight})


@login_required
def book_flight(request, flight_id):

    flight = get_object_or_404(Flight, pk=flight_id)

    if request.method == 'POST':

        seats_requested = int(request.POST.get('seats', 1))

        if seats_requested > flight.available_seats:

            messages.error(request, "Not enough seats")

            return redirect('flight_detail', flight_id=flight_id)

        request.session['seats_requested'] = seats_requested

        return redirect('seat_selection', flight_id=flight_id)

    return render(request, 'book_flight.html', {
        'flight': flight
    })


@login_required
def seat_selection(request, flight_id):

    flight = get_object_or_404(Flight, pk=flight_id)

    seats = Seat.objects.filter(flight=flight)

    if request.method == 'POST':

        selected_seats = request.POST.getlist('seats')

        seat_numbers = []

        for seat_id in selected_seats:

            seat = get_object_or_404(Seat, id=seat_id)

            if seat.is_booked:

                messages.error(request, "Seat already booked")

                return redirect('seat_selection', flight_id=flight_id)

            seat.is_booked = True
            seat.save()

            seat_numbers.append(seat.seat_number)

        total_price = flight.price * len(selected_seats)

        booking = Booking.objects.create(
            user=request.user,
            flight=flight,
            seats_booked=len(selected_seats),
            seat_number=",".join(seat_numbers),
            total_price=total_price
        )

        flight.available_seats -= len(selected_seats)

        flight.save()

        return redirect('confirm_booking', booking_id=booking.id)

    return render(request, 'seat_selection.html', {
        'flight': flight,
        'seats': seats
    })


@login_required
def my_bookings(request):

    bookings = Booking.objects.filter(user=request.user)

    return render(request, 'my_bookings.html', {
        'bookings': bookings
    })


@login_required
def confirm_booking(request, booking_id):

    booking = get_object_or_404(Booking, pk=booking_id)

    return render(request, 'confirm_booking.html', {
        'booking': booking
    })


# VIEW TICKET

@login_required
def view_ticket(request, booking_id):

    booking = get_object_or_404(Booking, pk=booking_id)

    return render(request, 'ticket.html', {
        'booking': booking
    })


# DOWNLOAD PROFESSIONAL PDF TICKET

@login_required
def download_ticket(request, booking_id):

    booking = get_object_or_404(Booking, pk=booking_id)

    template = get_template('ticket.html')

    html = template.render({
        'booking': booking
    })

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = (
        f'attachment; filename="ticket_{booking.id}.pdf"'
    )

    pisa_status = pisa.CreatePDF(
        html,
        dest=response
    )

    if pisa_status.err:
        return HttpResponse('Error generating PDF')

    return response


@login_required
def dashboard(request):

    flights = Flight.objects.all()

    total_flights = flights.count()

    total_available_seats = sum(
        f.available_seats for f in flights
    )

    total_bookings = Booking.objects.count()

    last_month_bookings = random.randint(80, 200)

    last_month_profit = random.randint(200000, 800000)

    growth_percentage = random.randint(10, 40)

    return render(request, 'dashboard.html', {

        'flights': flights,

        'total_flights': total_flights,

        'total_available_seats': total_available_seats,

        'total_bookings': total_bookings,

        'last_month_bookings': last_month_bookings,

        'last_month_profit': last_month_profit,

        'growth_percentage': growth_percentage,
    })


def register(request):

    if request.method == 'POST':

        username = request.POST.get('username')

        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():

            messages.error(request, "Username already exists")

            return redirect('register')

        User.objects.create_user(
            username=username,
            password=password
        )

        messages.success(request, "Registration successful")

        return redirect('login')

    return render(request, 'register.html')


def login_view(request):

    if request.method == 'POST':

        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )

        if user:

            login(request, user)

            return redirect('home')

        else:

            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


@login_required
def logout_view(request):

    logout(request)

    return redirect('login')