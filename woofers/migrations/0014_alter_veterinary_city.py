# Generated by Django 4.2.7 on 2024-03-03 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('woofers', '0013_alter_veterinary_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='veterinary',
            name='city',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='woofers.city'),
        ),
    ]