import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woofers.settings')
django.setup()

from woofers.models import Veterinary, Review, User  # replace with your actual app name
fake = Faker()

GENDER_CHOICES = ['M', 'F', 'O']

def create_user():
    user = User(
        email=fake.email(),
        username=fake.user_name(),
        password=fake.password()
    )
    user.save()

def create_veterinary():
    veterinary = Veterinary(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        email=fake.email(),
        location=fake.city(),
        gender=random.choice(GENDER_CHOICES),
        created_at=fake.date_time_this_year(),
        profile_picture=None  # You can add a default image path here
    )
    veterinary.save()

    # Create associated reviews
    for _ in range(random.randint(1, 5)):  # Randomly generate between 1 and 5 reviews
        user = User.objects.order_by('?').first()  # Randomly select a user
        review = Review(
            user=user,
            veterinary=veterinary,
            review=fake.text(),
            created_at=fake.date_time_this_year()
        )
        review.save()

def add_veterinaries(n=20):
    for _ in range(n):
        create_veterinary()

if __name__ == '__main__':
    add_veterinaries(20)
