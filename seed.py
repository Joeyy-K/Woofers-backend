import os
import django
import random
from faker import Faker
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from woofers import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woofers.settings')
django.setup()

def get_random_profile_picture():
    default_images_dir = os.path.join(settings.STATICFILES_DIRS[0], 'default_images')
    images = os.listdir(default_images_dir)
    return os.path.join('default_images', random.choice(images))

def seed_data():
    User = get_user_model()
    fake = Faker()
    
    # Create 30 User instances
    for _ in range(30):
        username = fake.unique.user_name()  # Generate a unique username
        email = fake.unique.email()  # Generate a unique email
        user, created = User.objects.get_or_create(email=email, defaults={'username': username})
        if created:
            user.profile_picture = get_random_profile_picture()
            password = make_password('SecurePassword123')  # Hash the password
            user.password = password
            user.save()

if __name__ == '__main__':
    seed_data()
