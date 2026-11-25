from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdminPers(admin.ModelAdmin):
    list_display = ("patient", "doctor", "appointment_date", "status", "duration_minutes")
    list_filter = ("status", "appointment_date", "doctor")
    search_fields = ("reason", "status", "patient__username", "doctor__username")
    date_hierarchy = "appointment_date"

    fieldsets = (
        ("Description", {
            "fields": ("reason", "status", "prescription")
        }),
        ("Date + Duration", {
            "fields": ("appointment_date", "duration_minutes")
        }),
        ("Patients/Doctors", {
            "fields": ("doctor", "patient")
        }),
        ("Planification", {
            "fields": ("created_at", "updated_at")
        }),
    )

    readonly_fields = ("created_at", "updated_at")
