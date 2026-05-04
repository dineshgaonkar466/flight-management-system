from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('flight/<int:flight_id>/', views.flight_detail, name='flight_detail'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('bookings/', views.my_bookings, name='my_bookings'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Seat selection
   path(
    'seat-selection/',
    views.seat_selection,
    name='seat_selection'
),

    # User Auth
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]