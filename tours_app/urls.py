from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('tour/<int:pk>/', views.tour_detail, name='tour_detail'),
    path('checkout/<int:departure_id>/', views.checkout, name='checkout'),
    path('wip/', views.wip, name='wip'),
    path('register/', views.register, name='register'),
    path('booking/success/<str:order_number>/', views.booking_success, name='booking_success'),
    path('booking/search/', views.booking_search, name='booking_search'),
]
