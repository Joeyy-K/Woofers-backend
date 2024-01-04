import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woofers.settings')
django.setup()

from woofers.models import Veterinary  # replace with your actual app name
fake = Faker()

GENDER_CHOICES = ['M', 'F', 'O']

def create_veterinary():
    veterinary = Veterinary(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        location=fake.city(),
        gender=random.choice(GENDER_CHOICES),
        created_at=fake.date_time_this_year()
    )
    veterinary.save()

def add_veterinaries(n=20):
    for _ in range(n):
        create_veterinary()

if __name__ == '__main__':
    add_veterinaries(20)
