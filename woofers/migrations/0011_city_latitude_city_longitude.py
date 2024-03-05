# Generated by Django 4.2.7 on 2024-03-03 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('woofers', '0010_remove_veterinary_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='city',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='city',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
