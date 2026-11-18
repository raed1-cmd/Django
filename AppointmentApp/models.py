from django.db import models
from AccountApp.models import Doctor, Patient


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirme"
        CANCELLED = "CANCELLED", "Annule"

    reason = models.TextField()
    prescription = models.FileField(
        blank=True,
        upload_to='prescription/'
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )
    duration_minutes = models.PositiveIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    appointment_date = models.DateTimeField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')