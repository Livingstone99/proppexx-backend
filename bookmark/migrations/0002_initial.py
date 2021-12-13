# Generated by Django 3.2 on 2021-06-08 10:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('property', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bookmark', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookmarkproperty',
            name='buyer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookmarkproperty',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='property.property'),
        ),
        migrations.AddField(
            model_name='bookmarkfeature',
            name='buyer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bookmarkfeature',
            name='features',
            field=models.ManyToManyField(to='property.Feature'),
        ),
        migrations.AlterUniqueTogether(
            name='bookmarkproperty',
            unique_together={('buyer', 'property')},
        ),
    ]
