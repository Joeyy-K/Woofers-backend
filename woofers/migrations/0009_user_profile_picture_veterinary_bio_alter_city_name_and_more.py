# Generated by Django 4.2.7 on 2024-02-22 01:30

from django.db import migrations, models
import woofers.models


class Migration(migrations.Migration):

    dependencies = [
        ('woofers', '0008_country_city_veterinary_city'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(default=woofers.models.get_random_profile_picture, upload_to='user_pictures/'),
        ),
        migrations.AddField(
            model_name='veterinary',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='veterinary',
            name='profile_picture',
            field=models.ImageField(default=woofers.models.get_default_profile_picture, upload_to='veterinary_pictures/'),
        ),
    ]