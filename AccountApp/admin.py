from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Doctor, Patient, Speciality
from AppointmentApp.models import Appointment


class AppointmentStacked(admin.StackedInline):
    # Utilise admin.TabularInline pour un affichage en tableau
    model = Appointment
    extra = 1


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "license_number", "phone")
    search_fields = ("username", "first_name", "last_name", "license_number")
    filter_horizontal = ("specialities",)
    inlines = [AppointmentStacked]


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ("username", "first_name", "last_name", "national_id", "phone", "birth_date")
    search_fields = ("username", "first_name", "last_name", "national_id")
    list_filter = ("birth_date",)
    inlines = [AppointmentStacked]