import os
import random
import django
from faker import Faker


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woofers.settings')
django.setup()

from woofers.models import City, Veterinary

def get_default_profile_picture(instance=None):
    if instance is None:
        return os.path.join('default_images', 'default.jpg')
    elif instance.gender == 'M':
        return os.path.join('default_images', 'default_male.jpg')
    elif instance.gender == 'F':
        return os.path.join('default_images', 'default_female.jpg')
    else:
        return os.path.join('default_images', 'default_other.jpg')

def seed_data():
    # Get all cities
    cities = City.objects.all()

    # Create 30 Veterinary instances
    fake = Faker()
    for i in range(40):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.unique.email()  # Generate a unique email
        city = cities[i % len(cities)]  # This will cycle through the cities list
        gender = random.choice(['M', 'F', 'O'])
        bio = fake.text()
        vet = Veterinary(
            first_name=first_name,
            last_name=last_name,
            email=email,
            city=city,
            gender=gender,
            bio=bio
        )
        vet.profile_picture = get_default_profile_picture(vet)
        vet.save()

if __name__ == '__main__':
    seed_data()