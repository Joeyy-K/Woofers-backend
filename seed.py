import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woofers.settings')
django.setup()

from woofers.models import Veterinary, City, Country

def seed_data():
    # Create Kenya country instance
    kenya, created = Country.objects.get_or_create(name='Kenya')

    # List of cities in Kenya
    cities_in_kenya = ['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret']  # add more cities

    # Create City instances for each city in Kenya
    for city_name in cities_in_kenya:
        City.objects.get_or_create(name=city_name, country=kenya)

    # Get all veterinarians
    vets = Veterinary.objects.all()

    # Get all cities
    cities = City.objects.all()

    # Assign each vet to a city
    for i, vet in enumerate(vets):
        vet.city = cities[i % len(cities)]  # This will cycle through the cities list
        vet.save()

if __name__ == '__main__':
    seed_data()
