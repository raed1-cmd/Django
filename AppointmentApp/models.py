from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from AccountApp.models import Doctor, Patient


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

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
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    class Meta:
        ordering = ["appointment_date"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date"],
                name="unique_doctor_appointment_date",
                violation_error_message="Ce docteur a déjà un rendez-vous à cette date."
            )
        ]

    def clean(self):
        # La date est "modifiée" si c'est un nouveau rdv,
        # ou si la date enregistrée en base est différente de la nouvelle.
        modified_date = self._state.adding or not (
            Appointment.objects.filter(
                pk=self.pk,
                appointment_date=self.appointment_date
            ).exists()
        )
        if modified_date and self.appointment_date <= timezone.now():
            raise ValidationError(
                "La date du rendez-vous doit être supérieure à la date d'aujourd'hui."
            )

    def __str__(self):
        return f"{self.patient} - {self.doctor} - {self.appointment_date}"