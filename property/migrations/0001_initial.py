# Generated by Django 3.2 on 2021-06-08 10:35

import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import users.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(editable=False, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('purpose', models.CharField(choices=[('rent', 'Rent'), ('sale', 'Sale')], max_length=20)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('bedroom', models.PositiveIntegerField(default=0)),
                ('bathroom', models.PositiveIntegerField(default=0)),
                ('parlour', models.PositiveIntegerField(default=0)),
                ('kitchen', models.PositiveIntegerField(default=0)),
                ('toilet', models.PositiveIntegerField(default=0)),
                ('draft', models.BooleanField(default=False)),
                ('available', models.BooleanField(default=False)),
                ('featured', models.BooleanField(default=False)),
                ('append_to', models.CharField(choices=[('daily', 'daily'), ('monthly', 'monthly'), ('yearly', 'yearly'), ('sqm', 'sqm')], max_length=30)),
                ('virtual_reality', models.TextField(blank=True, null=True)),
                ('size', models.CharField(max_length=10)),
                ('document', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=10)),
                ('video_link', models.URLField(blank=True, null=True)),
                ('keyword', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), blank=True, null=True, size=10)),
                ('country', models.CharField(max_length=150)),
                ('state', models.CharField(blank=True, max_length=40, null=True)),
                ('lGA', models.CharField(blank=True, max_length=100, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('address', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(editable=False, null=True)),
                ('active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('published', 'published'), ('sold', 'sold')], default='publish', max_length=10)),
                ('longitude', models.DecimalField(blank=True, decimal_places=16, max_digits=22)),
                ('latitude', models.DecimalField(blank=True, decimal_places=16, max_digits=22)),
                ('location', django.contrib.gis.db.models.fields.PointField(blank=True, default=django.contrib.gis.geos.point.Point(0, 0), srid=4326)),
            ],
            options={
                'verbose_name_plural': "Agents' Properties",
                'get_latest_by': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=users.utils.upload_property_path, validators=[users.utils.validate_document])),
            ],
        ),
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(editable=False, null=True)),
            ],
            options={
                'verbose_name_plural': 'Property types',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property')),
            ],
        ),
    ]
