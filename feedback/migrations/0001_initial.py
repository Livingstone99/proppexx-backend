# Generated by Django 3.2 on 2021-06-08 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_id', models.CharField(max_length=10, unique=True)),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField(max_length=500)),
                ('has_replied', models.BooleanField(default=False)),
                ('reply', models.TextField(blank=True, max_length=500, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'get_latest_by': ['created_at'],
            },
        ),
    ]
