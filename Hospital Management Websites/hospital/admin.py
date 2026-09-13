from django.contrib import admin
from .models import Appointment, ContactMessage, CareerApplication, PatientProfile, ChatLog


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'department', 'preferred_date', 'preferred_time', 'status', 'created_at')
    list_filter = ('status', 'department')
    search_fields = ('full_name', 'email', 'phone')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'email', 'is_read', 'created_at')
    list_filter = ('is_read',)
    search_fields = ('name', 'email', 'subject')


@admin.register(CareerApplication)
class CareerApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'years_experience', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'email', 'position')


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'gender', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')


@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('session_id', 'user_message', 'created_at')
    search_fields = ('user_message', 'bot_response')
