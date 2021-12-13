# Generated by Django 3.2 on 2021-06-08 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('paid', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('assigned', 'assigned'), ('reviewed', 'reviewed')], default='pending', max_length=10)),
                ('refrence_code', models.CharField(blank=True, max_length=15, null=True)),
            ],
        ),
    ]
