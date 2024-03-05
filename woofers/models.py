from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import os
import random
from django.conf import settings


def get_random_profile_picture():
    default_images_dir = os.path.join(settings.STATICFILES_DIRS[0], 'default_images')
    images = os.listdir(default_images_dir)
    return os.path.join('default_images', random.choice(images))

class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture = models.ImageField(upload_to='user_pictures/', default=get_random_profile_picture)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(unique=True, max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    ...


def get_default_profile_picture(instance=None):
    if instance is None:
        return os.path.join('default_images', 'default.jpg')
    elif instance.gender == 'M':
        return os.path.join('default_images', 'default_male.jpg')
    elif instance.gender == 'F':
        return os.path.join('default_images', 'default_female.jpg')
    else:
        return os.path.join('default_images', 'default_other.jpg')

class Veterinary(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    bio = models.TextField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='veterinary_pictures/', default=get_default_profile_picture)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    veterinary = models.ForeignKey(Veterinary, on_delete=models.CASCADE, related_name='reviews')
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return f'Review by {self.user.email} for {self.veterinary.first_name} {self.veterinary.last_name}'
    
class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    veterinary = models.ForeignKey(Veterinary, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    reason_for_visit = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Appointment for {self.user.email} with {self.veterinary.first_name} {self.veterinary.last_name} on {self.date} at {self.time}'

