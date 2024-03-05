import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'woofers.settings')
django.setup()

from woofers.models import City

def update_city_coordinates():
    cities_coordinates = {
        'Nairobi': (-1.286389, 36.817223),
        'Mombasa': (-3.97682910, 39.71371810),
        'Kisumu': (-0.09170160, 34.76795680),
        'Nakuru': (-0.303099, 36.080025),
        'Eldoret': (0.52036000, 35.26993000),
        'Nyeri': (-0.4201, 36.9476),
        'Machakos': (-1.51768370, 37.26341460),
        'Meru': (0.35571740, 37.80876930),
    }

    for city_name, coordinates in cities_coordinates.items():
        try:
            city = City.objects.get(name=city_name)
            city.latitude, city.longitude = coordinates
            city.save()
            print(f"Updated coordinates for {city_name}")
        except City.DoesNotExist:
            print(f"City {city_name} does not exist in the database")

if __name__ == "__main__":
    update_city_coordinates()
