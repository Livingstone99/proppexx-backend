# Generated by Django 3.2 on 2021-10-30 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0022_alter_property_purpose'),
    ]

    operations = [
        migrations.AlterField(
            model_name='property',
            name='purpose',
            field=models.CharField(choices=[('rent', 'Rent'), ('sale', 'sale')], max_length=20),
        ),
    ]
