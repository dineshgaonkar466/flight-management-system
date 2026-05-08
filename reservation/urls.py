from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('confirm/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('bookings/', views.my_bookings, name='my_bookings'),
    path('ticket/<int:booking_id>/', views.download_ticket, name='download_ticket'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # ✅ Seat selection (FIXED)
    path('seat-selection/<int:flight_id>/', views.seat_selection, name='seat_selection'),

    # User Auth
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]