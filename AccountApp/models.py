from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


number_validator = RegexValidator(
    regex=r'^\d{8}$',
    message="Le numéro doit contenir exactement 8 chiffres."
)


def validate_birth_date(value):
    if value > timezone.now().date():
        raise ValidationError("La date de naissance ne peut pas être dans le futur.")


class User(AbstractUser):
    pass


class Speciality(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Doctor(User):
    license_number = models.CharField(max_length=6, unique=True)
    phone = models.CharField(max_length=8, validators=[number_validator])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    specialities = models.ManyToManyField(Speciality, related_name='doctors')


class Patient(User):
    national_id = models.CharField(max_length=8, unique=True, validators=[number_validator])
    phone = models.CharField(max_length=8, validators=[number_validator])
    birth_date = models.DateField(validators=[validate_birth_date])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)