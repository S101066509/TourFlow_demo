from django.contrib import admin
from .models import Location, Tag, Tour, Departure, Order, Banner
'''
註冊後台管理項目
'''
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active')
    list_editable = ('order', 'is_active')

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'days', 'is_active')
    list_filter = ('location', 'is_active')
    filter_horizontal = ('tags',)

@admin.register(Departure)
class DepartureAdmin(admin.ModelAdmin):
    list_display = ('tour', 'start_date', 'price', 'available_seats')
    list_filter = ('start_date', 'tour')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_name', 'departure', 'pax', 'total_price', 'created_at')
    list_filter = ('created_at',)
